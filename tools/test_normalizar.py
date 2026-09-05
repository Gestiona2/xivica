"""Pruebas de la normalizacion de productos. Se corren con:
       python3 -m unittest discover tools -v
   Usan unittest de la biblioteca estandar a proposito: sin dependencias que
   instalar, el proyecto se puede verificar en cualquier maquina."""
import unittest

from normalizar import normalizar_precio, hacer_slug, normalizar_producto


class PrecioTest(unittest.TestCase):
    def test_formato_colombiano_a_entero(self):
        self.assertEqual(normalizar_precio("$62,900.00"), 62900)
        self.assertEqual(normalizar_precio("$8,200.00"), 8200)
        self.assertEqual(normalizar_precio("$1,234,567.00"), 1234567)

    def test_ausente_es_none(self):
        self.assertIsNone(normalizar_precio(None))
        self.assertIsNone(normalizar_precio(""))
        self.assertIsNone(normalizar_precio("Consultar"))


class SlugTest(unittest.TestCase):
    def test_sin_tildes_ni_simbolos(self):
        self.assertEqual(hacer_slug("ACID MANTLE N LOCIÓN 120 ML"),
                         "acid-mantle-n-locion-120-ml")
        self.assertEqual(hacer_slug("CRE.DEPILEX 3EN1 (2X1)"), "cre-depilex-3en1-2x1")

    def test_sin_guiones_repetidos_ni_en_los_bordes(self):
        self.assertEqual(hacer_slug("  ...HOLA -- MUNDO...  "), "hola-mundo")


class ProductoTest(unittest.TestCase):
    crudo = {
        "t": "OSCILLOCOCCINUM", "p": "$62,900.00", "antes": "$84,915.00",
        "c": "Medicamentos", "img": "img/a.webp", "imgs": ["img/a.webp"],
        "d": "desc", "slug": "oscillococcinum",
    }

    def test_precio_entero_y_descuento_calculado(self):
        p = normalizar_producto(self.crudo)
        self.assertEqual(p["precio"], 62900)
        self.assertEqual(p["precio_antes"], 84915)
        self.assertEqual(p["descuento"], 26)

    def test_categoria_y_imagenes_normalizadas(self):
        p = normalizar_producto(self.crudo)
        self.assertEqual(p["categoria"], "medicamentos")
        self.assertEqual(p["imagenes"], ["a.webp"])

    def test_sin_precio_anterior_no_hay_descuento(self):
        crudo = dict(self.crudo)
        del crudo["antes"]
        p = normalizar_producto(crudo)
        self.assertIsNone(p["precio_antes"])
        self.assertIsNone(p["descuento"])

    def test_rx_arranca_pendiente_nunca_inferido(self):
        # Afirmar que un medicamento no requiere formula es un riesgo legal:
        # el dato nace vacio y solo lo llena una revision humana.
        p = normalizar_producto(self.crudo)
        self.assertIsNone(p["rx"])
        self.assertEqual(p["origen"]["rx"], "pendiente")


if __name__ == "__main__":
    unittest.main()
