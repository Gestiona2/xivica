"""Pruebas del validador del catalogo.
   python3 -m unittest discover tools -v"""
import unittest

from validar import validar

BUENO = {
    "slug": "abc", "titulo": "ABC", "precio": 1000, "precio_antes": None,
    "descuento": None, "categoria": "medicamentos", "imagenes": ["a.webp"],
    "descripcion": "x", "stock": True, "rx": None,
}


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


if __name__ == "__main__":
    unittest.main()
