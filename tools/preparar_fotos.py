#!/usr/bin/env python3
"""Prepara una foto para la web: la recorta, la reduce y la guarda en WebP.

    python3 tools/preparar_fotos.py ORIGEN NOMBRE [--relacion 4:3] [--centro 0.5,0.3]
                                                  [--recorte x0,y0,x1,y1]

    ORIGEN   la foto tal como llega (JPG, PNG, la que mande el cliente por WhatsApp)
    NOMBRE   donde queda dentro de public/img, sin extension. Por ejemplo
             fotos/fachada-tejares-del-norte

HERRAMIENTA LOCAL: se corre en el computador de quien edita, no en el servidor.

Por que existe: una foto de celular pesa 300 KB a 1 MB y mide 1500 px o mas.
Subirla tal cual haria lenta la pagina, sobre todo en un celular con datos.
Aqui se recorta a la forma que necesita el sitio, se genera una version chica y
una grande (el navegador elige la que le sirve) y se borran los metadatos.

    --relacion  forma final: 4:3 (tarjetas), 3:2 (fotos anchas), 16:9, 1:1 (circulos)
    --centro    que parte de la foto conservar al recortar, de 0 a 1 en x,y.
                0.5,0.5 es el centro; 0.5,0 es pegado arriba. Por defecto, el centro.
    --recorte   caja exacta en pixeles de la foto original. Manda sobre --relacion.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

# El sitio muestra tarjetas de ~330 px y fotos anchas de ~760 px, y un celular
# de alta densidad necesita ~1,75 veces eso. El escalon de 900 evita que el
# celular tenga que bajar la version de 1200 cuando le basta con menos.
ANCHOS = (600, 900, 1200)
ANCHO_MINIMO = 600
CALIDAD = 80

# Carpeta de imagenes del sitio, relativa a la raiz del proyecto.
CARPETA_IMG = Path(__file__).resolve().parent.parent / "public" / "img"


def _leer_relacion(texto):
    """'4:3' -> (4, 3). Cualquier otra cosa es un error que se entiende."""
    try:
        ancho, alto = (float(parte) for parte in texto.split(":"))
    except (ValueError, AttributeError):
        raise ValueError(f"La relación '{texto}' no es válida. Se escribe así: 4:3") from None
    if ancho <= 0 or alto <= 0:
        raise ValueError(f"La relación '{texto}' no es válida: ningún lado puede ser cero.")
    return ancho, alto


def caja_de_recorte(ancho, alto, relacion, centro=(0.5, 0.5)):
    """La caja (x0, y0, x1, y1) mas grande que cabe en la foto con esa relacion.

    Conserva todo el ancho o todo el alto, lo que se pueda, y elige que parte
    dejar con `centro`. Nunca se sale de la foto.
    """
    ancho_rel, alto_rel = _leer_relacion(relacion)
    objetivo = ancho_rel / alto_rel

    if ancho / alto > objetivo:              # la foto es mas ancha que lo pedido
        alto_caja, ancho_caja = alto, round(alto * objetivo)
    else:                                    # la foto es mas alta que lo pedido
        ancho_caja, alto_caja = ancho, round(ancho / objetivo)

    cx = min(max(centro[0], 0.0), 1.0)
    cy = min(max(centro[1], 0.0), 1.0)
    x0 = round((ancho - ancho_caja) * cx)
    y0 = round((alto - alto_caja) * cy)
    return x0, y0, x0 + ancho_caja, y0 + alto_caja


def _anchos_de_salida(ancho_recorte):
    """Los tamanos a generar, sin estirar nunca la foto.

    Si el recorte no llega a 1200, el tamano grande es el propio recorte.
    """
    if ancho_recorte < ANCHO_MINIMO:
        raise ValueError(
            f"La foto es muy pequeña ({ancho_recorte} px de ancho tras recortar): "
            f"se vería borrosa. Hace falta al menos {ANCHO_MINIMO} px."
        )
    # Un tamano chico solo vale la pena si es claramente mas chico que el grande;
    # si se parecen, seria el mismo archivo dos veces.
    chicos = {w for w in ANCHOS if w < ancho_recorte * 0.8}
    return sorted(chicos | {min(max(ANCHOS), ancho_recorte)})


def preparar(origen, nombre, destino=CARPETA_IMG, relacion=None, centro=(0.5, 0.5), recorte=None):
    """Recorta y reduce una foto. Devuelve la lista de archivos creados."""
    origen = Path(origen)
    if not origen.exists():
        raise FileNotFoundError(f"La foto '{origen}' no existe.")

    with Image.open(origen) as original:
        # Los celulares guardan la foto "acostada" y anotan como girarla en los
        # metadatos. Si no se corrige aqui, una foto vertical sale horizontal.
        imagen = ImageOps.exif_transpose(original).convert("RGB")

    if recorte:
        caja = tuple(int(v) for v in recorte)
    elif relacion:
        caja = caja_de_recorte(*imagen.size, relacion, centro)
    else:
        caja = (0, 0, *imagen.size)
    imagen = imagen.crop(caja)

    salida = Path(destino) / nombre
    salida.parent.mkdir(parents=True, exist_ok=True)

    archivos = []
    for ancho in _anchos_de_salida(imagen.width):
        alto = round(imagen.height * ancho / imagen.width)
        version = imagen.resize((ancho, alto), Image.LANCZOS) if ancho != imagen.width else imagen
        archivo = salida.with_name(f"{salida.name}-{ancho}.webp")
        # No se pasa exif: el WebP nace sin ubicacion, fecha ni modelo de celular.
        version.save(archivo, "WEBP", quality=CALIDAD, method=6)
        archivos.append(archivo)
    return archivos


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prepara una foto para la web.")
    parser.add_argument("origen")
    parser.add_argument("nombre", help="ruta dentro de public/img, sin extensión")
    parser.add_argument("--relacion", help="forma final, por ejemplo 4:3")
    parser.add_argument("--centro", default="0.5,0.5", help="parte a conservar, por ejemplo 0.5,0.2")
    parser.add_argument("--recorte", help="caja en píxeles: x0,y0,x1,y1")
    args = parser.parse_args(argv)

    try:
        centro = tuple(float(v) for v in args.centro.split(","))
        recorte = tuple(int(v) for v in args.recorte.split(",")) if args.recorte else None
        archivos = preparar(args.origen, args.nombre, relacion=args.relacion,
                            centro=centro, recorte=recorte)
    except (ValueError, FileNotFoundError) as error:
        print(f"No se pudo preparar la foto: {error}")
        return 1

    for archivo in archivos:
        with Image.open(archivo) as im:
            print(f"  {archivo.relative_to(CARPETA_IMG)}  {im.width}x{im.height}  "
                  f"{archivo.stat().st_size // 1024} KB")
    print(f'\nEn el sitio se usa como  "foto": "{args.nombre}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
