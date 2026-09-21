"""Pruebas de la preparacion de fotos.
   python3 -m unittest discover tools -v"""
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from preparar_fotos import caja_de_recorte, preparar


def foto_de_prueba(carpeta, ancho, alto, orientacion=None, nombre="origen.jpg"):
    """Una foto sintetica. Con `orientacion` simula una foto de celular girada."""
    imagen = Image.new("RGB", (ancho, alto), (200, 120, 40))
    ruta = Path(carpeta) / nombre
    if orientacion:
        exif = Image.Exif()
        exif[0x0112] = orientacion
        imagen.save(ruta, "JPEG", exif=exif.tobytes())
    else:
        imagen.save(ruta, "JPEG")
    return ruta


class CajaDeRecorteTest(unittest.TestCase):
    def test_cuadrada_a_cuatro_tercios_conserva_el_ancho_y_centra(self):
        x0, y0, x1, y1 = caja_de_recorte(1500, 1500, "4:3")
        self.assertEqual((x0, x1), (0, 1500))
        self.assertAlmostEqual((y1 - y0) / (x1 - x0), 3 / 4, places=2)
        self.assertLessEqual(abs(y0 - (1500 - y1)), 1)  # centrada

    def test_horizontal_a_cuadrado_conserva_el_alto_y_centra(self):
        x0, y0, x1, y1 = caja_de_recorte(1600, 900, "1:1")
        self.assertEqual((y0, y1), (0, 900))
        self.assertEqual(x1 - x0, 900)
        self.assertLessEqual(abs(x0 - (1600 - x1)), 1)

    def test_el_centro_desplaza_el_recorte(self):
        # centro (0.5, 0) = pegado arriba: lo que importa esta en la parte alta
        _, y0, _, _ = caja_de_recorte(1500, 1500, "4:3", centro=(0.5, 0.0))
        self.assertEqual(y0, 0)

    def test_el_recorte_nunca_se_sale_de_la_foto(self):
        for centro in [(0, 0), (1, 1), (0.5, 1.0), (1.0, 0.5)]:
            x0, y0, x1, y1 = caja_de_recorte(1500, 1500, "16:9", centro=centro)
            self.assertGreaterEqual(x0, 0)
            self.assertGreaterEqual(y0, 0)
            self.assertLessEqual(x1, 1500)
            self.assertLessEqual(y1, 1500)

    def test_relacion_mal_escrita_es_error_claro(self):
        with self.assertRaisesRegex(ValueError, "relación"):
            caja_de_recorte(1500, 1500, "cuadrado")
        with self.assertRaisesRegex(ValueError, "relación"):
            caja_de_recorte(1500, 1500, "0:3")


class PrepararTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.salida = self.dir / "img"

    def tearDown(self):
        self._tmp.cleanup()

    def test_genera_tres_tamanos_en_webp_con_la_relacion_pedida(self):
        # 600 / 900 / 1200: en un celular de 390 px con pantalla de alta densidad
        # hacen falta ~700 px. Sin el de 900 el navegador saltaba al de 1200.
        origen = foto_de_prueba(self.dir, 2000, 1500)
        archivos = preparar(origen, "fotos/prueba", self.salida, relacion="4:3")

        nombres = sorted(a.name for a in archivos)
        self.assertEqual(nombres, ["prueba-1200.webp", "prueba-600.webp", "prueba-900.webp"])
        for archivo in archivos:
            with Image.open(archivo) as im:
                self.assertEqual(im.format, "WEBP")
                self.assertAlmostEqual(im.height / im.width, 3 / 4, places=2)
        with Image.open(self.salida / "fotos" / "prueba-1200.webp") as im:
            self.assertEqual(im.width, 1200)

    def test_no_amplia_una_foto_pequena(self):
        origen = foto_de_prueba(self.dir, 900, 900)
        archivos = preparar(origen, "fotos/chica", self.salida)
        anchos = sorted(Image.open(a).width for a in archivos)
        self.assertEqual(anchos, [600, 900])   # el grande es el original, no 1200 estirado

    def test_si_el_chico_casi_no_se_diferencia_del_grande_no_se_genera(self):
        # Un recorte de 650 px con una version de 600 seria el mismo archivo dos
        # veces: el navegador no ganaria nada eligiendo entre ellos.
        origen = foto_de_prueba(self.dir, 650, 650)
        archivos = preparar(origen, "fotos/casi", self.salida)
        self.assertEqual([Image.open(a).width for a in archivos], [650])

    def test_foto_demasiado_pequena_se_rechaza(self):
        origen = foto_de_prueba(self.dir, 500, 500)
        with self.assertRaisesRegex(ValueError, "pequeña"):
            preparar(origen, "fotos/minima", self.salida)

    def test_recorte_en_pixeles_manda_sobre_la_relacion(self):
        origen = foto_de_prueba(self.dir, 2000, 1500)
        archivos = preparar(
            origen, "fotos/caja", self.salida, recorte=(500, 100, 1500, 1100), relacion="16:9"
        )
        with Image.open(max(archivos, key=lambda a: Image.open(a).width)) as im:
            self.assertEqual((im.width, im.height), (1000, 1000))

    def test_respeta_la_orientacion_de_los_celulares(self):
        # Orientation=6: el celular guardo la foto girada. Sin corregirla,
        # una foto vertical saldria acostada en la web.
        origen = foto_de_prueba(self.dir, 2000, 1400, orientacion=6)
        archivos = preparar(origen, "fotos/girada", self.salida)
        with Image.open(max(archivos, key=lambda a: Image.open(a).width)) as im:
            self.assertGreater(im.height, im.width)

    def test_no_deja_metadatos_de_la_foto_original(self):
        origen = foto_de_prueba(self.dir, 2000, 1400, orientacion=6)
        for archivo in preparar(origen, "fotos/limpia", self.salida):
            with Image.open(archivo) as im:
                self.assertEqual(len(im.getexif()), 0)

    def test_origen_inexistente_es_error_claro(self):
        with self.assertRaisesRegex(FileNotFoundError, "no existe"):
            preparar(self.dir / "nada.jpg", "fotos/x", self.salida)


if __name__ == "__main__":
    unittest.main()
