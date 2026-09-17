"""Pruebas del validador del catalogo.
   python3 -m unittest discover tools -v"""
import unittest

import json
import tempfile
from pathlib import Path

from validar import validar, leer_catalogo

BUENO = {
    "slug": "abc", "titulo": "ABC", "precio": 1000, "precio_antes": None,
    "descuento": None, "categoria": "medicamentos", "imagenes": ["a.webp"],
    "descripcion": "x", "stock": True, "rx": None, "destacado": False,
}
CATEGORIAS = {"medicamentos", "cuidado-personal"}


class ValidarTest(unittest.TestCase):
    def test_producto_correcto_no_da_errores(self):
        self.assertEqual(validar([BUENO]), [])

    def test_precio_como_texto_es_error(self):
        malo = dict(BUENO, precio="$1.000")
        self.assertTrue(any("precio" in e for e in validar([malo])))

    def test_precio_cero_o_negativo_es_error(self):
        self.assertTrue(any("precio" in e for e in validar([dict(BUENO, precio=0)])))
        self.assertTrue(any("precio" in e for e in validar([dict(BUENO, precio=-5)])))

    def test_slug_repetido_es_error(self):
        errores = validar([BUENO, dict(BUENO)])
        self.assertTrue(any("repetido" in e for e in errores))

    def test_slug_con_mayusculas_o_espacios_es_error(self):
        self.assertTrue(any("slug" in e for e in validar([dict(BUENO, slug="Con Espacio")])))

    def test_sin_imagenes_es_error(self):
        self.assertTrue(any("imagen" in e for e in validar([dict(BUENO, imagenes=[])])))

    def test_campo_obligatorio_ausente_es_error(self):
        sin_titulo = {k: v for k, v in BUENO.items() if k != "titulo"}
        self.assertTrue(any("titulo" in e for e in validar([sin_titulo])))

    def test_descuento_incoherente_es_error(self):
        # precio mayor que el precio anterior no es una oferta
        malo = dict(BUENO, precio=2000, precio_antes=1000, descuento=50)
        self.assertTrue(any("precio_antes" in e for e in validar([malo])))

    def test_el_error_dice_de_que_producto_se_trata(self):
        errores = validar([dict(BUENO, slug="paracetamol-500", precio=0)])
        self.assertTrue(any("paracetamol-500" in e for e in errores))

    def test_imagen_inexistente_es_error_si_se_pide_revisar(self):
        errores = validar([BUENO], carpeta_imagenes="/carpeta/que/no/existe")
        self.assertTrue(any("no existe" in e for e in errores))


class CamposQueAntesSeEscapabanTest(unittest.TestCase):
    """Cada uno de estos errores se publicaba sin aviso antes de 2026-09-14."""

    def test_rx_como_texto_es_error(self):
        # El mas grave: "si" no es true, y un medicamento de control saldria
        # en la portada saltandose la regla legal.
        errores = validar([dict(BUENO, rx="si")])
        self.assertTrue(any("rx" in e for e in errores))

    def test_rx_acepta_true_false_y_vacio(self):
        for valor in (True, False, None):
            self.assertEqual(validar([dict(BUENO, rx=valor)]), [], valor)

    def test_stock_como_texto_es_error(self):
        self.assertTrue(any("stock" in e for e in validar([dict(BUENO, stock="no")])))

    def test_destacado_como_texto_es_error(self):
        self.assertTrue(any("destacado" in e for e in validar([dict(BUENO, destacado="true")])))

    def test_promo_flash_como_texto_es_error(self):
        self.assertTrue(any("promo_flash" in e for e in validar([dict(BUENO, promo_flash="si")])))

    def test_promo_flash_acepta_true_false_y_ausente(self):
        for valor in (True, False, None):
            producto = dict(BUENO)
            if valor is None:
                producto.pop("promo_flash", None)
            else:
                producto["promo_flash"] = valor
            self.assertEqual(validar([producto]), [], valor)

    def test_promo_flash_con_formula_o_sin_existencias_es_error(self):
        self.assertTrue(any("promo_flash" in e for e in validar([dict(BUENO, promo_flash=True, rx=True)])))
        self.assertTrue(any("promo_flash" in e for e in validar([dict(BUENO, promo_flash=True, stock=False)])))

    def test_titulo_vacio_es_error(self):
        self.assertTrue(any("titulo" in e for e in validar([dict(BUENO, titulo="  ")])))

    def test_categoria_inexistente_es_error_y_sugiere(self):
        errores = validar([dict(BUENO, categoria="medicamento")], categorias=CATEGORIAS)
        self.assertTrue(any("medicamento" in e and "medicamentos" in e for e in errores), errores)

    def test_categoria_existente_pasa(self):
        self.assertEqual(validar([BUENO], categorias=CATEGORIAS), [])

    def test_descuento_que_no_cuadra_con_los_precios_es_error(self):
        malo = dict(BUENO, precio=62900, precio_antes=84915, descuento=90)
        errores = validar([malo])
        # El mensaje dice el valor correcto, para corregirlo sin calcular.
        self.assertTrue(any("descuento" in e and "26" in e for e in errores), errores)

    def test_descuento_correcto_pasa(self):
        self.assertEqual(validar([dict(BUENO, precio=62900, precio_antes=84915, descuento=26)]), [])

    def test_descuento_sin_precio_anterior_es_error(self):
        self.assertTrue(any("descuento" in e for e in validar([dict(BUENO, descuento=20)])))

    def test_precio_anterior_sin_descuento_es_error(self):
        malo = dict(BUENO, precio=62900, precio_antes=84915, descuento=None)
        self.assertTrue(any("descuento" in e for e in validar([malo])))


class PrecioSospechosoTest(unittest.TestCase):
    def test_precio_con_ceros_de_mas_es_error(self):
        # 62900 escrito como 629000000: sin oferta, ninguna otra regla lo ve.
        errores = validar([dict(BUENO, precio=629000000)])
        self.assertTrue(any("ceros" in e for e in errores), errores)

    def test_el_producto_mas_caro_del_catalogo_pasa(self):
        self.assertEqual(validar([dict(BUENO, precio=240000)]), [])


class SintaxisTest(unittest.TestCase):
    def _leer(self, texto):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            f.write(texto)
        return leer_catalogo(Path(f.name))

    def test_json_roto_da_linea_y_explicacion_legible(self):
        productos, error = self._leer('[\n {"slug": "a",,\n  "titulo": "A"}\n]')
        self.assertIsNone(productos)
        self.assertIn("línea 2", error)
        self.assertNotIn("Traceback", error)

    def test_comilla_sin_cerrar_se_explica_en_espanol(self):
        productos, error = self._leer('[\n {"slug": "a",\n  "titulo": "A\n}]')
        self.assertIn("comilla", error)

    def test_json_correcto_se_lee(self):
        productos, error = self._leer(json.dumps([BUENO]))
        self.assertIsNone(error)
        self.assertEqual(len(productos), 1)


if __name__ == "__main__":
    unittest.main()
