#!/usr/bin/env python3
"""Deriva campos adicionales del catalogo para poder filtrar de verdad.

    python3 tools/enriquecer.py src/datos/productos.json

La regla de esta herramienta es la trazabilidad: cada campo derivado queda
anotado en `origen` con de donde salio, para que se pueda auditar sin abrir
cuatrocientos productos uno por uno.

    "titulo"    leido literal del nombre del producto. Fiable.
    "inferido"  deducido por palabras clave. Revisable, puede fallar.
    "pendiente" no se deduce: lo llena una persona.
    "revisado"  confirmado por el regente de farmacia.

Lo que esta herramienta NO hace, a proposito: decidir si un producto requiere
formula medica. Ese campo se queda en "pendiente" hasta que lo confirme el
regente. Marcar de menos un medicamento de control no es un error de datos,
es un problema legal.
"""
import json
import re
import sys
from pathlib import Path

# --- Formas farmaceuticas, leidas literal del titulo ------------------------
FORMAS = [
    (r"\bTAB(?:LETAS?|S)?\b|\bTBS\b|\bCOMPRIMIDOS?\b", "Tabletas"),
    (r"\bGRAGEAS?\b", "Grageas"),
    (r"\bCAP(?:SULAS?|S)?\b", "Cápsulas"),
    (r"\b(?:JBE|JARABE)\b", "Jarabe"),
    (r"\bCREMA\b", "Crema"),
    (r"\bUNGUENTO\b|\bPOMADA\b", "Ungüento"),
    (r"\bGEL\b", "Gel"),
    (r"\bLOCION\b", "Loción"),
    (r"\bGOTAS\b", "Gotas"),
    (r"\bSOBRES?\b|\bSBS\b", "Sobres"),
    (r"\bAMP(?:OLLAS?)?\b", "Ampollas"),
    (r"\bOVULOS?\b", "Óvulos"),
    (r"\bSUPOSITORIOS?\b", "Supositorios"),
    (r"\bSUSP(?:ENSION)?\b", "Suspensión"),
    (r"\bSHAMPOO\b|\bCHAMPU\b|\bCHA\.", "Shampoo"),
    (r"\bSPRAY\b", "Spray"),
    (r"\bPOLVO\b", "Polvo"),
]

# --- Subcategorias, inferidas por palabras clave ----------------------------
# Se revisan en orden: la primera que coincide gana.
SUBCATEGORIAS = [
    ("analgesicos", ["ACETAMINOFEN", "IBUPROFENO", "NAPROXENO", "DOLEX", "ADVIL",
                     "ASPIRINA", "DICLOFENACO", "VOLTAREN", "NEOSALDINA", "CALMIDOL",
                     "PIROXICAM", "ANALGES", "DOLOR", "MIGRA"]),
    ("antigripales", ["GRIPA", "NOXPIRIN", "SINUTAB", "CORICIDIN", "DESENFRIOL",
                      "ANTIGRIPAL", "TUKOL", "VICK", "TOS", "EXPECTORANTE",
                      "OSCILLOCOCCINUM", "AMBROXOL", "ABRILAR"]),
    ("antibioticos", ["AMOXICILINA", "AZITROMICINA", "CEFALEXINA", "CIPROFLOXACINO",
                      "CLAVULIN", "DOXICICLINA", "PENICILINA", "TRIMETOPRIM"]),
    ("gastrointestinal", ["OMEPRAZOL", "PANTOPRAZOL", "RANITIDINA", "ANTIACIDO",
                          "MILANTA", "BUSCAPINA", "ENTEROGERMINA", "FLORATIL",
                          "LOPERAMIDA", "ELECTROLIT", "SUERO", "LAXANTE", "DIGESTIVO"]),
    ("cardiovascular", ["LOSARTAN", "AMLODIPINO", "ENALAPRIL", "ATORVASTATINA",
                        "METOPROLOL", "CARDIOASPIRINA", "VALSARTAN", "HIDROCLOROTIAZIDA"]),
    ("diabetes", ["METFORMINA", "GLIBENCLAMIDA", "INSULINA", "GLUCOMETRO"]),
    ("antialergicos", ["LORATADINA", "CETIRIZINA", "CLARITIN", "ALERGIA",
                       "HIDROXICINA", "DESLORATADINA"]),
    ("dermatologicos", ["ANTIMICOTICO", "UNESIA", "MICOSIS", "HONGOS", "TRIGENTAX",
                        "LOMECAN", "CANESTEN", "DERMICO", "ACID MANTLE"]),
    ("anticonceptivos", ["ANTICONCEPTIVO", "SLINDA", "YAEL", "DROSPIRENONA",
                         "LEVONORGESTREL", "CONDON", "PRESERVATIVO", "DUREX"]),
    ("vitaminas", ["VITAMINA", "CENTRUM", "OMEGA", "CALCIO", "HIERRO", "ZINC",
                   "MAGNESIO", "REDOXON", "COLAGENO", "MULTIVITAMIN", "SHOT B",
                   "CEREBRIT", "VITACEREBRINA", "COMPLEJO B"]),
    ("bebe", ["PAÑAL", "PANAL", "HUGGIES", "PAMPERS", "NAN ", "NESTUM", "JJ BABY",
              "JOHNSON", "TETERO", "BEBE", "INFANTIL", "PEDIATRIC"]),
    ("higiene-femenina", ["TOALLA", "TAMPON", "TAMP.", "NOSOTRAS", "KOTEX",
                          "PROTECTOR", "INTIMA"]),
    ("cuidado-capilar", ["SHAMPOO", "CHAMPU", "CHA.", "ACONDICIONADOR", "SEDAL",
                         "TIO NACHO", "TINTE", "CABELLO", "H&S", "HS2"]),
    ("cuidado-piel", ["CREMA", "LOCION", "NIVEA", "LUBRIDERM", "PONDS", "HIDRATANTE",
                      "BLOQUEADOR", "SUNSTOP", "PROTECTOR SOLAR", "SPF"]),
    ("cuidado-bucal", ["CREMA DENTAL", "COLGATE", "ORAL B", "ENJUAGUE", "CEPILLO",
                       "SEDA DENTAL", "LISTERINE"]),
    ("desodorantes", ["DESODORANTE", "REXONA", "DOVE", "TALCO", "MEXSANA", "ANTITRANS"]),
    ("adulto-mayor", ["TENA", "WINNY", "INCONTINENCIA", "PROTECCION ADULTO"]),
    ("antivirales", ["ACICLOVIR", "VALACICLOVIR", "OSELTAMIVIR", "ANTIVIRAL"]),
    ("suplementos", ["ACIDO FOLICO", "PROTEINA", "ENSURE", "GLUCERNA", "PEDIASURE",
                     "CREATINA", "AMINOACIDO", "FIBRA", "PROBIOTICO"]),
    ("respiratorio", ["SALBUTAMOL", "INHALADOR", "BUDESONIDA", "ASMA", "NEBULIZ",
                      "LORATADIN", "MUCOSINA", "AFLUX", "AMBROXOL", "BROMHEXINA"]),
    ("tiroides-hormonal", ["EUTIROX", "LEVOTIROXINA", "TIROIDES", "ESTRADIOL",
                           "TESTOSTERONA", "PROGESTERONA"]),
    ("salud-visual", ["OFTALMICA", "OFTALMICO", "LAGRIMAS", "OCULAR", "EYE ",
                      "COLIRIO", "GOTAS OJOS"]),
    ("salud-sexual", ["SILDENAFIL", "TADALAFIL", "VIAGRA", "LUBRICANTE", "EROXIM"]),
    ("bucal-aftas", ["AFTA", "ENCIAS", "GINGIVAL", "BUCAL"]),
    ("botiquin", ["CURITA", "GASA", "ALCOHOL", "AGUA OXIGENADA", "VENDA", "JERINGA",
                  "TERMOMETRO", "TAPABOCA", "ALGODON", "ISODINE", "YODO"]),
]

MARCAS = [
    "NIVEA", "LUBRIDERM", "PONDS", "SEDAL", "COLGATE", "REXONA", "DOVE", "JOHNSON",
    "HUGGIES", "PAMPERS", "NESTLE", "NAN", "CENTRUM", "REDOXON", "VICK", "DOLEX",
    "ADVIL", "ASPIRINA", "CARDIOASPIRINA", "VOLTAREN", "BUSCAPINA", "MILANTA",
    "TENA", "WINNY", "NOSOTRAS", "KOTEX", "LISTERINE", "MEXSANA", "TIO NACHO",
    "ENTEROGERMINA", "FLORATIL", "ELECTROLIT", "CLARITIN", "CANESTEN", "DUREX",
    "NEOSALDINA", "CALMIDOL", "TUKOL", "CORICIDIN", "SINUTAB", "NOXPIRIN",
    "LOMECAN", "UNESIA", "TRIGENTAX", "ABRILAR", "OSCILLOCOCCINUM", "SUNSTOP",
    "CEREBRIT", "VITACEREBRINA", "SLINDA", "CLAVULIN", "NESTUM", "ISODINE",
]


def extraer_presentacion(titulo):
    """Devuelve la presentacion leida literal del titulo, o None.

    Ejemplos: 'ACETAMINOFEN 500 MG X 20 TAB' -> '500 mg · 20 Tabletas'
              'CREMA NIVEA BODY MILK 125 ML'  -> '125 ml'
    """
    partes = []

    dosis = re.search(r"\b(\d+(?:[.,]\d+)?)\s*MG\b", titulo, re.I)
    if dosis:
        partes.append(f"{dosis.group(1)} mg")
    else:
        micro = re.search(r"\b(\d+(?:[.,]\d+)?)\s*MCG\b", titulo, re.I)
        if micro:
            partes.append(f"{micro.group(1)} mcg")

    volumen = re.search(r"\b(\d+(?:[.,]\d+)?)\s*ML\b", titulo, re.I)
    if volumen:
        partes.append(f"{volumen.group(1)} ml")

    peso = re.search(r"\b(\d+(?:[.,]\d+)?)\s*GR?\b", titulo, re.I)
    if peso and not volumen:
        partes.append(f"{peso.group(1)} g")

    forma = None
    for patron, nombre in FORMAS:
        if re.search(patron, titulo, re.I):
            forma = nombre
            break

    cantidad = re.search(r"\bX\s*(\d+)\b", titulo, re.I)
    if not cantidad:
        # 'NAPROXENO 250 MG 10 CAPSULAS' — el numero va antes de la forma
        cantidad = re.search(
            r"\b(\d+)\s*(?:TAB|TBS|CAPS|CAPSULAS|TABLETAS|COMPRIMIDOS|GRAGEAS|"
            r"SOBRES|SBS|UDS|UND|SUPOSITORIOS)\b",
            titulo, re.I)

    if cantidad and forma:
        partes.append(f"{cantidad.group(1)} {forma}")
    elif cantidad:
        partes.append(f"{cantidad.group(1)} unidades")
    elif forma:
        partes.append(forma)

    return " · ".join(partes) if partes else None


def extraer_marca(titulo):
    """Devuelve la marca si aparece literal en el titulo."""
    limpio = titulo.upper()
    for marca in MARCAS:
        if re.search(rf"\b{re.escape(marca)}\b", limpio):
            return marca.title()
    return None


def inferir_subcategoria(titulo, categoria):
    """Deduce la subcategoria por palabras clave. Puede fallar: va como 'inferido'."""
    limpio = titulo.upper()
    for nombre, claves in SUBCATEGORIAS:
        if any(clave in limpio for clave in claves):
            return nombre
    return None


def enriquecer(producto):
    titulo = producto["titulo"]
    origen = dict(producto.get("origen") or {})

    presentacion = extraer_presentacion(titulo)
    if presentacion:
        producto["presentacion"] = presentacion
        origen["presentacion"] = "titulo"

    marca = extraer_marca(titulo)
    if marca:
        producto["marca"] = marca
        origen["marca"] = "titulo"

    subcategoria = inferir_subcategoria(titulo, producto["categoria"])
    if subcategoria:
        producto["subcategoria"] = subcategoria
        origen["subcategoria"] = "inferido"

    # Ofertas es un estado, no una categoria: se sabe por el descuento.
    if producto["categoria"] in ("ofertas", "sin-categorizar"):
        producto["categoria"] = "varios"
        origen["categoria"] = "corregido"

    origen.setdefault("rx", "pendiente")
    producto["origen"] = origen
    return producto


def main(ruta):
    productos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    productos = [enriquecer(p) for p in productos]
    Path(ruta).write_text(
        json.dumps(productos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    total = len(productos)
    con = lambda campo: sum(1 for p in productos if p.get(campo))
    print(f"{total} productos enriquecidos en {ruta}\n")
    print(f"  presentacion  {con('presentacion'):4}  ({con('presentacion')*100//total}%)  leido del titulo")
    print(f"  marca         {con('marca'):4}  ({con('marca')*100//total}%)  leido del titulo")
    print(f"  subcategoria  {con('subcategoria'):4}  ({con('subcategoria')*100//total}%)  inferido, revisable")
    print(f"  rx            {con('rx'):4}  pendiente de revision del regente")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
