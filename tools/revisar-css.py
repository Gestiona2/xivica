#!/usr/bin/env python3
"""Revisa que todas las variables de color usadas existan de verdad.

    python3 tools/revisar-css.py

Existe por una razon concreta: se escribieron 31 usos de var(--borde) cuando
la variable se llamaba --border, y el CSS invalido no da error en ninguna
parte. Simplemente los bordes dejan de verse y nadie se entera hasta que
alguien mira la pagina con atencion.
"""
import re
import sys
from pathlib import Path

# Variables que define el JavaScript en tiempo de ejecucion, no el CSS.
EN_JAVASCRIPT = {"--i"}


def revisar(carpeta="src/styles"):
    css = "\n".join(p.read_text(encoding="utf-8") for p in sorted(Path(carpeta).glob("*.css")))
    definidas = set(re.findall(r"^\s*(--[a-z0-9-]+)\s*:", css, re.M))
    usadas = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    return sorted(usadas - definidas - EN_JAVASCRIPT)


if __name__ == "__main__":
    faltan = revisar()
    if faltan:
        print("Variables de CSS usadas pero nunca definidas:\n")
        for variable in faltan:
            print(f"  {variable}")
        print("\nEl navegador las ignora en silencio: el estilo simplemente no se aplica.")
        sys.exit(1)
    print("Todas las variables de CSS usadas están definidas")
