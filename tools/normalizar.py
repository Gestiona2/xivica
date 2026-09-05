#!/usr/bin/env python3
"""Convierte el catalogo heredado (productos_v2.json) al modelo del sitio nuevo.

HERRAMIENTA LOCAL: se ejecuta en el equipo de quien construye, una sola vez.
No se sube al hosting y el sitio publicado no la necesita para nada.

    python3 tools/normalizar.py <entrada.json> <salida.json>

El cambio de fondo frente al catalogo viejo es que los precios dejan de ser
texto ("$62,900.00") y pasan a enteros en pesos (62900). Guardarlos como texto
obligaba a desarmar la cadena para poder ordenar, filtrar o sumar.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

# El catalogo heredado trae los precios siempre con dos decimales: "$62,900.00".
# Al quitar todo lo que no sea digito quedan los centavos pegados, por eso se
# dividen entre cien. Si algun dia la fuente cambiara de formato, esta es la
# linea que hay que revisar primero.
CENTAVOS = 100


def normalizar_precio(texto):
    """'$62,900.00' -> 62900. Devuelve None si no hay un precio utilizable."""
    if not texto:
        return None
    digitos = re.sub(r"[^0-9]", "", str(texto))
    if not digitos:
        return None
    return int(digitos) // CENTAVOS


def hacer_slug(titulo):
    """'ACID MANTLE N LOCIÓN 120 ML' -> 'acid-mantle-n-locion-120-ml'."""
    limpio = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    limpio = re.sub(r"[^a-zA-Z0-9]+", "-", limpio)
    return re.sub(r"-{2,}", "-", limpio).strip("-").lower()


def normalizar_producto(crudo):
    """Una entrada del catalogo viejo -> una entrada del modelo nuevo."""
    precio = normalizar_precio(crudo.get("p"))
    antes = normalizar_precio(crudo.get("antes"))

    descuento = None
    if antes and precio and antes > precio:
        descuento = round((antes - precio) / antes * 100)

    imagenes = [i for i in (crudo.get("imgs") or [crudo.get("img")]) if i]
    imagenes = [i.replace("img/", "") for i in imagenes]

    return {
        "slug": crudo.get("slug") or hacer_slug(crudo["t"]),
        "titulo": crudo["t"].strip(),
        "precio": precio,
        "precio_antes": antes,
        "descuento": descuento,
        "categoria": hacer_slug(crudo.get("c") or "sin-categoria"),
        "subcategoria": None,
        "marca": None,
        "presentacion": None,
        # rx = requiere formula medica. Nace vacio y solo lo llena el regente
        # de farmacia. Ver tools/enriquecer.py y PENDIENTES.md.
        "rx": None,
        "stock": True,
        "imagenes": imagenes,
        "descripcion": (crudo.get("d") or "").strip(),
        "origen": {"rx": "pendiente"},
    }


def unificar_slugs(productos):
    """Garantiza que no haya dos productos con el mismo slug.

    Importa mas de lo que parece: cada slug es una URL, y dos productos con el
    mismo slug significan una pagina menos publicada, en silencio.
    """
    vistos = {}
    for producto in productos:
        base = producto["slug"]
        if base in vistos:
            vistos[base] += 1
            producto["slug"] = f"{base}-{vistos[base]}"
        else:
            vistos[base] = 1
    return productos


def main(entrada, salida):
    crudos = json.loads(Path(entrada).read_text(encoding="utf-8"))
    productos = unificar_slugs([normalizar_producto(c) for c in crudos])
    Path(salida).write_text(
        json.dumps(productos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"{len(productos)} productos escritos en {salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
