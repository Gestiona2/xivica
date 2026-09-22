"""Prueba de extremo a extremo de excel_catalogo.py: generar -> revisar -> aplicar.

   python3 -m unittest discover tools -v

Existe porque `openpyxl` faltaba en tools/requirements.txt y nada lo notó: la
herramienta nunca se importaba desde ninguna prueba, así que el hueco solo
se habría visto el día que el agente del cliente la usara por primera vez, en
la máquina del cliente. Esta prueba importa el módulo de verdad y ejerce sus
tres funciones contra un archivo .xlsx real, así que un `pip install` que
falte se ve aquí, no en producción.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import excel_catalogo as ec  # noqa: E402  (después de ajustar sys.path)

PRODUCTOS = [
    {
        "slug": "producto-uno", "titulo": "PRODUCTO UNO", "marca": "Acme",
        "presentacion": "30 Tabletas", "categoria": "medicamentos", "subcategoria": None,
        "precio": 10000, "precio_antes": None, "descuento": None,
        "stock": True, "destacado": False, "promo_flash": False, "rx": None,
        "imagenes": ["uno.webp"], "descripcion": "x", "origen": {"rx": "pendiente"},
    },
    {
        "slug": "producto-dos", "titulo": "PRODUCTO DOS", "marca": None,
        "presentacion": None, "categoria": "cuidado-personal", "subcategoria": None,
        "precio": 8000, "precio_antes": 10000, "descuento": 20,
        "stock": True, "destacado": False, "promo_flash": False, "rx": None,
        "imagenes": ["dos.webp"], "descripcion": "y", "origen": {"rx": "pendiente"},
    },
]
CATEGORIAS = [{"id": "medicamentos"}, {"id": "cuidado-personal"}]


class ExcelCatalogoTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        raiz = Path(self._tmp.name)
        self.json_path = raiz / "productos.json"
        self.xlsx_path = raiz / "catalogo.xlsx"
        self.json_path.write_text(json.dumps(PRODUCTOS, ensure_ascii=False), encoding="utf-8")
        (raiz / "categorias.json").write_text(json.dumps(CATEGORIAS), encoding="utf-8")

        # RUTA_JSON/RUTA_XLSX son globales del modulo, apuntando al catalogo
        # real. Se cambian por las de la prueba y se restauran al terminar.
        self._json_original, self._xlsx_original = ec.RUTA_JSON, ec.RUTA_XLSX
        ec.RUTA_JSON, ec.RUTA_XLSX = self.json_path, self.xlsx_path

    def tearDown(self):
        ec.RUTA_JSON, ec.RUTA_XLSX = self._json_original, self._xlsx_original
        self._tmp.cleanup()

    def test_generar_crea_una_planilla_legible(self):
        ec.generar()
        self.assertTrue(self.xlsx_path.exists())

        filas = ec.leer_filas(self.xlsx_path)
        self.assertEqual(len(filas), 2)
        self.assertEqual(filas[0]["slug"], "producto-uno")
        # El SI/NO se escribe en la planilla como texto, no como True/False.
        self.assertEqual(filas[0]["stock"], "SI")

    def test_revisar_sin_tocar_nada_no_encuentra_problemas(self):
        ec.generar()
        self.assertEqual(ec.revisar(self.xlsx_path), 0)

    def test_aplicar_un_cambio_real_queda_en_el_json(self):
        ec.generar()

        libro = ec.load_workbook(self.xlsx_path)
        hoja = libro["Productos"]
        # Columna G = precio (ver COLUMNAS). Sube el primer producto a 12.000.
        hoja["G2"] = 12000
        libro.save(self.xlsx_path)

        self.assertEqual(ec.aplicar(self.xlsx_path), 0)
        productos = json.loads(self.json_path.read_text(encoding="utf-8"))
        self.assertEqual(productos[0]["precio"], 12000)
        # Lo que no se tocó en la planilla no cambia en el catálogo.
        self.assertEqual(productos[1]["precio"], 8000)

    def test_un_precio_invalido_no_se_aplica_a_nada(self):
        ec.generar()

        libro = ec.load_workbook(self.xlsx_path)
        hoja = libro["Productos"]
        hoja["G2"] = "doce mil"  # no es un número
        libro.save(self.xlsx_path)

        self.assertEqual(ec.aplicar(self.xlsx_path), 1)
        # El catálogo queda exactamente como estaba: nada a medias.
        productos = json.loads(self.json_path.read_text(encoding="utf-8"))
        self.assertEqual(productos[0]["precio"], 10000)

    def test_borrar_una_fila_es_error_no_una_eliminacion_silenciosa(self):
        ec.generar()

        libro = ec.load_workbook(self.xlsx_path)
        hoja = libro["Productos"]
        hoja.delete_rows(3)  # borra la fila de producto-dos
        libro.save(self.xlsx_path)

        self.assertEqual(ec.revisar(self.xlsx_path), 1)

    def test_de_si_no_y_de_rx_no_dejan_pasar_cualquier_texto(self):
        errores = []
        self.assertEqual(ec.de_si_no("tal vez", "stock", "x", errores), (False, False))
        self.assertEqual(len(errores), 1)

        errores = []
        valor, ok = ec.de_rx("", "x", errores)
        self.assertIsNone(valor)
        self.assertTrue(ok)  # vacío es válido: significa "sin revisar todavía"


if __name__ == "__main__":
    unittest.main()
