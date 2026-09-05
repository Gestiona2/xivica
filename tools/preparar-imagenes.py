#!/usr/bin/env python3
"""Copia a public/img solo las imagenes que el catalogo usa de verdad.

    python3 tools/preparar-imagenes.py <carpeta-origen> [--limite-kb 90]

HERRAMIENTA LOCAL: no se sube al hosting.

La carpeta heredada tiene 1.265 archivos porque guarda cada imagen dos veces,
en .jpg y en .webp, mas variantes de tamano que ya no se usan. Aqui se copia
una sola version por producto, prefiriendo WebP, y se avisa de las que pesan
mas de lo razonable para que se optimicen.
"""
import json
import shutil
import sys
from pathlib import Path


def elegir_archivo(nombre, origen):
    """Devuelve la mejor version disponible de una imagen, prefiriendo WebP."""
    candidato = origen / nombre
    if candidato.suffix.lower() != ".webp":
        webp = candidato.with_suffix(".webp")
        if webp.exists():
            return webp
    if candidato.exists():
        return candidato
    # A veces el catalogo apunta a un tamano que no existe pero si otro.
    for alterna in origen.glob(candidato.stem.rsplit("-", 1)[0] + "*"):
        if alterna.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png"):
            return alterna
    return None


def main(origen, catalogo, destino, limite_kb):
    origen, destino = Path(origen), Path(destino)
    destino.mkdir(parents=True, exist_ok=True)

    productos = json.loads(Path(catalogo).read_text(encoding="utf-8"))
    necesarias = {img for p in productos for img in p["imagenes"]}

    copiadas, faltantes, pesadas = 0, [], []
    for nombre in sorted(necesarias):
        archivo = elegir_archivo(nombre, origen)
        if not archivo:
            faltantes.append(nombre)
            continue
        shutil.copy2(archivo, destino / nombre)
        copiadas += 1
        kb = (destino / nombre).stat().st_size // 1024
        if kb > limite_kb:
            pesadas.append((nombre, kb))

    total_mb = sum(f.stat().st_size for f in destino.iterdir()) / 1_048_576
    print(f"{copiadas} imagenes copiadas a {destino} ({total_mb:.1f} MB)")
    print(f"referenciadas por el catalogo: {len(necesarias)}")

    if faltantes:
        print(f"\nFALTAN {len(faltantes)} imagenes:")
        for nombre in faltantes[:20]:
            print(f"  - {nombre}")

    if pesadas:
        pesadas.sort(key=lambda x: -x[1])
        print(f"\n{len(pesadas)} imagenes pesan mas de {limite_kb} KB:")
        for nombre, kb in pesadas[:10]:
            print(f"  - {nombre} ({kb} KB)")

    return 1 if faltantes else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    limite = 90
    if "--limite-kb" in sys.argv:
        limite = int(sys.argv[sys.argv.index("--limite-kb") + 1])
    sys.exit(main(sys.argv[1], "src/datos/productos.json", "public/img", limite))
