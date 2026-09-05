#!/usr/bin/env python3
"""Revisa que el catalogo este bien formado antes de publicarlo.

    python3 tools/validar.py src/datos/productos.json

Existe porque el catalogo lo edita un agente conversando con el dueno de la
drogueria, y una coma mal puesta o un precio escrito como texto romperia la
tienda para todos los visitantes. La accion de GitHub corre este script en
cada cambio: si algo esta mal, el sitio no se publica y produccion sigue
funcionando con la version anterior.

Devuelve codigo de salida 1 si hay errores, para que la accion falle.
"""
import json
import re
import sys
from pathlib import Path

OBLIGATORIOS = ("slug", "titulo", "precio", "categoria", "imagenes")
SLUG_VALIDO = re.compile(r"^[a-z0-9-]+$")


def validar(productos, carpeta_imagenes=None):
    """Devuelve la lista de errores encontrados. Vacia significa que todo esta bien.

    Cada mensaje nombra el producto para poder ubicarlo entre cuatrocientos.
    """
    errores = []
    vistos = set()

    for indice, producto in enumerate(productos):
        quien = producto.get("slug") or producto.get("titulo") or f"producto #{indice}"

        for campo in OBLIGATORIOS:
            if campo not in producto:
                errores.append(f"{quien}: falta el campo obligatorio '{campo}'")

        slug = producto.get("slug")
        if slug is not None:
            if not isinstance(slug, str) or not SLUG_VALIDO.match(slug):
                errores.append(
                    f"{quien}: el slug debe ser minusculas, numeros y guiones "
                    f"(es la URL del producto)"
                )
            elif slug in vistos:
                errores.append(f"{quien}: slug repetido, cada producto necesita el suyo")
            else:
                vistos.add(slug)

        precio = producto.get("precio")
        if not isinstance(precio, int) or isinstance(precio, bool) or precio <= 0:
            errores.append(
                f"{quien}: el precio debe ser un numero entero de pesos mayor que cero "
                f"(por ejemplo 62900, no \"$62.900\")"
            )

        antes = producto.get("precio_antes")
        if antes is not None:
            if not isinstance(antes, int) or isinstance(antes, bool):
                errores.append(f"{quien}: precio_antes debe ser un numero entero o estar vacio")
            elif isinstance(precio, int) and not isinstance(precio, bool) and antes <= precio:
                errores.append(
                    f"{quien}: precio_antes ({antes}) no es mayor que el precio ({precio}), "
                    f"asi que no hay oferta que mostrar"
                )

        imagenes = producto.get("imagenes")
        if not isinstance(imagenes, list) or not imagenes:
            errores.append(f"{quien}: necesita al menos una imagen")
        elif carpeta_imagenes:
            for imagen in imagenes:
                if not (Path(carpeta_imagenes) / imagen).exists():
                    errores.append(f"{quien}: la imagen '{imagen}' no existe en la carpeta")

    return errores


def main(ruta, carpeta_imagenes=None):
    productos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    errores = validar(productos, carpeta_imagenes)

    if errores:
        print(f"{len(errores)} problema(s) en {ruta}:\n")
        for error in errores[:60]:
            print(f"  - {error}")
        if len(errores) > 60:
            print(f"  ... y {len(errores) - 60} mas")
        return 1

    print(f"{len(productos)} productos validos en {ruta}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    carpeta = sys.argv[2] if len(sys.argv) > 2 else None
    sys.exit(main(sys.argv[1], carpeta))
