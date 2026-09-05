# Plan de implementación — Droguería Xivica

> **Para quien ejecute este plan:** usar `superpowers:subagent-driven-development` o
> `superpowers:executing-plans`. Los pasos llevan casilla (`- [ ]`) para seguimiento.

**Objetivo:** construir el sitio de Droguería Xivica en Astro, con 407 páginas de producto
indexables, catálogo filtrable, carrito que cierra por WhatsApp y datos en JSON versionado.

**Arquitectura:** sitio estático generado por Astro 7 desde `src/datos/*.json`. Todo el
contenido editable vive en esos JSON; ningún `.astro` lleva texto escrito directamente.
El JavaScript de cliente son módulos ES sueltos que se hidratan sobre el HTML ya generado.

**Stack:** Astro 7, Tailwind 4 (`@theme`), JS vanilla en módulos ES, Leaflet para mapas,
Python 3.12 solo para herramientas de construcción locales.

**Spec:** `docs/2026-09-04-web-xivica-design.md`

## Restricciones globales

- **Partir de** `generador/plantillas/astro-base/`, no de un proyecto en blanco.
- **Ningún texto dentro de los `.astro`.** Todo en `src/datos/`, un archivo por página.
- **Ningún color escrito directo.** Solo `var(--…)` definidas en `src/styles/global.css`.
- **Fuentes auto-hospedadas** en `/public/fonts`, nunca desde Google Fonts.
- **El lima `#a0c030` no se usa como texto sobre fondo claro** — no alcanza contraste AA.
- **Precios como enteros en pesos.** Se formatean al mostrar con `Intl.NumberFormat('es-CO')`.
- **`base` configurable** por `PUBLIC_BASE`: `/xivica/` en el demo, `/` en producción.
- **Imágenes faltantes** con `placehold.co` a la medida correcta, anotadas en `PENDIENTES.md`.
- **Nada de `tools/` se publica.** Son herramientas locales.
- **Rutas siempre entre comillas** en los comandos: las carpetas tienen espacios.
- **Nunca afirmar que algo funciona sin haberlo comprobado.**

---

### Tarea 1: Andamiaje y tokens de marca

**Archivos:**
- Copiar: `generador/plantillas/astro-base/` → raíz de `web-xivica/`
- Modificar: `package.json`, `astro.config.mjs`, `src/styles/global.css`
- Crear: `public/fonts/archivo-variable.woff2`, `.gitignore`

**Interfaces:**
- Produce: los tokens `--azul`, `--azul-hondo`, `--cian`, `--lima`, `--tinta`, `--linea`,
  y las variables semánticas `--bg`, `--surface`, `--texto`, `--texto-2`, `--borde`,
  que todas las tareas siguientes consumen.

- [ ] **Paso 1: copiar la plantilla base**

```bash
cd "/mnt/5ddaa367-d44e-4462-8632-c0f57f33031c/DESARROLLO/PAGINAS WEB IA/base_web_ia"
cp -r "generador/plantillas/astro-base/." "web-xivica/"
```

- [ ] **Paso 2: ajustar `package.json`**

Cambiar `"name"` a `"web-xivica"`. Dejar las dependencias como están (Astro 7, Tailwind 4).

- [ ] **Paso 3: `astro.config.mjs` con `base` configurable**

```js
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: process.env.PUBLIC_SITE || "https://gestiona2.github.io",
  base: process.env.PUBLIC_BASE || "/",
  vite: { plugins: [tailwindcss()] },
});
```

- [ ] **Paso 4: descargar la fuente Archivo variable, subset latino**

```bash
cd "/mnt/5ddaa367-d44e-4462-8632-c0f57f33031c/DESARROLLO/PAGINAS WEB IA/base_web_ia/web-xivica"
curl -sL "https://cdn.jsdelivr.net/fontsource/fonts/archivo:vf@latest/latin-wght-normal.woff2" \
  -o public/fonts/archivo-variable.woff2
ls -l public/fonts/archivo-variable.woff2
```

Esperado: un archivo de entre 20 y 60 KB. Si sale vacío o falla, anotarlo en
`PENDIENTES.md` y dejar `system-ui` como fuente hasta resolverlo.

- [ ] **Paso 5: escribir los tokens en `src/styles/global.css`**

Reemplazar los bloques `@font-face`, `@theme` y `:root` de la plantilla por:

```css
@font-face {
  font-family: "Archivo";
  font-style: normal;
  font-weight: 400 800;
  font-display: swap;
  src: url("/fonts/archivo-variable.woff2") format("woff2");
}

@theme {
  --font-display: "Archivo", ui-sans-serif, system-ui, sans-serif;
  --font-body: "Archivo", ui-sans-serif, system-ui, sans-serif;

  --color-azul: #0b4da2;
  --color-azul-hondo: #08356f;
  --color-cian: #00a0e0;
  --color-lima: #a0c030;
  --color-tinta: #16202b;
}

:root {
  --azul: #0b4da2;
  --azul-hondo: #08356f;
  --cian: #00a0e0;
  --lima: #a0c030;
  --lima-hondo: #87a821;
  --lima-tinta: #16300a;   /* texto sobre lima — único uso accesible */
  --tinta: #16202b;
  --texto: #16202b;
  --texto-2: #66788a;
  --borde: #e6ebef;
  --bg: #ffffff;
  --bg-soft: #f2f6f9;
  --surface: #ffffff;
  --rojo: #e23b2e;         /* solo descuentos */

  --sombra-card: 0 10px 22px -14px rgba(11, 77, 162, 0.4);
  --sombra-alta: 0 20px 40px -22px rgba(11, 77, 162, 0.45);
  --radio: 10px;
  --ancho: 1320px;
}
```

- [ ] **Paso 6: verificar que compila**

```bash
cd "/mnt/5ddaa367-d44e-4462-8632-c0f57f33031c/DESARROLLO/PAGINAS WEB IA/base_web_ia/web-xivica"
npm install && npm run build
```

Esperado: `Complete!` sin errores.

- [ ] **Paso 7: commit**

```bash
git add -A && git commit -m "Andamiaje Astro y tokens de marca de Xivica"
```

---

### Tarea 2: Normalizar los datos de productos

Convierte el JSON heredado al modelo del spec. Es la base de todo lo demás, y por eso
lleva pruebas de verdad.

**Archivos:**
- Crear: `tools/normalizar.py`, `tools/test_normalizar.py`, `data/schema.json`
- Produce: `src/datos/productos.json`

**Interfaces:**
- Produce: `normalizar_precio(texto) -> int`, `hacer_slug(titulo) -> str`,
  `normalizar_producto(dict) -> dict` con las claves del spec.

- [ ] **Paso 1: escribir la prueba que falla**

`tools/test_normalizar.py`:

```python
from normalizar import normalizar_precio, hacer_slug, normalizar_producto

def test_precio_con_formato_colombiano():
    assert normalizar_precio("$62,900.00") == 62900
    assert normalizar_precio("$8,200.00") == 8200
    assert normalizar_precio("$1,234,567.00") == 1234567

def test_precio_ausente_es_none():
    assert normalizar_precio(None) is None
    assert normalizar_precio("") is None

def test_slug_sin_tildes_ni_simbolos():
    assert hacer_slug("ACID MANTLE N LOCIÓN 120 ML") == "acid-mantle-n-locion-120-ml"
    assert hacer_slug("CRE.DEPILEX 3EN1 (2X1)") == "cre-depilex-3en1-2x1"

def test_producto_conserva_precio_como_entero():
    crudo = {
        "t": "OSCILLOCOCCINUM", "p": "$62,900.00", "antes": "$84,915.00",
        "c": "Medicamentos", "img": "img/a.webp", "imgs": ["img/a.webp"],
        "d": "desc", "slug": "oscillococcinum",
    }
    p = normalizar_producto(crudo)
    assert p["precio"] == 62900
    assert p["precio_antes"] == 84915
    assert p["categoria"] == "medicamentos"
    assert p["imagenes"] == ["a.webp"]
    assert p["descuento"] == 26   # (84915-62900)/84915 redondeado
```

- [ ] **Paso 2: comprobar que falla**

```bash
cd "/mnt/5ddaa367-d44e-4462-8632-c0f57f33031c/DESARROLLO/PAGINAS WEB IA/base_web_ia/web-xivica/tools"
python3 -m pytest test_normalizar.py -v
```

Esperado: FALLA con `ModuleNotFoundError: No module named 'normalizar'`.

- [ ] **Paso 3: escribir `tools/normalizar.py`**

```python
"""Convierte productos_v2.json (heredado) al modelo del spec."""
import json, re, sys, unicodedata
from pathlib import Path

def normalizar_precio(texto):
    if not texto:
        return None
    digitos = re.sub(r"[^0-9]", "", str(texto))
    if not digitos:
        return None
    return int(digitos) // 100      # el formato trae siempre dos decimales

def hacer_slug(titulo):
    s = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)

def normalizar_producto(crudo):
    precio = normalizar_precio(crudo.get("p"))
    antes = normalizar_precio(crudo.get("antes"))
    descuento = round((antes - precio) / antes * 100) if antes and precio else None
    return {
        "slug": crudo.get("slug") or hacer_slug(crudo["t"]),
        "titulo": crudo["t"].strip(),
        "precio": precio,
        "precio_antes": antes,
        "descuento": descuento,
        "categoria": hacer_slug(crudo.get("c", "sin-categoria")),
        "imagenes": [i.replace("img/", "") for i in crudo.get("imgs") or [crudo.get("img")] if i],
        "descripcion": crudo.get("d", "").strip(),
        "stock": True,
    }

def main(entrada, salida):
    crudos = json.loads(Path(entrada).read_text(encoding="utf-8"))
    productos = [normalizar_producto(c) for c in crudos]
    vistos, unicos = set(), []
    for p in productos:
        if p["slug"] in vistos:
            p["slug"] = f"{p['slug']}-{len(unicos)}"
        vistos.add(p["slug"])
        unicos.append(p)
    Path(salida).write_text(
        json.dumps(unicos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(unicos)} productos escritos en {salida}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

- [ ] **Paso 4: comprobar que pasa**

```bash
python3 -m pytest test_normalizar.py -v
```

Esperado: 4 pruebas PASAN.

- [ ] **Paso 5: generar el archivo real y verificar el resultado**

```bash
cd "/mnt/5ddaa367-d44e-4462-8632-c0f57f33031c/DESARROLLO/PAGINAS WEB IA/base_web_ia/web-xivica"
python3 tools/normalizar.py \
  "../../drogueria/insumos/productos_v2.json" \
  "src/datos/productos.json"
python3 -c "
import json; d=json.load(open('src/datos/productos.json'))
assert len(d)==407, len(d)
assert len({p['slug'] for p in d})==407, 'slugs repetidos'
assert all(isinstance(p['precio'],int) for p in d), 'precio no entero'
print('407 productos, slugs unicos, precios enteros')
print('rango de precios:', min(p['precio'] for p in d), '-', max(p['precio'] for p in d))
"
```

Esperado: sin errores, y un rango de precios plausible (miles a cientos de miles).
**Si el rango sale absurdo, el divisor `// 100` está mal y hay que revisarlo antes de seguir.**

- [ ] **Paso 6: commit**

```bash
git add tools/ src/datos/productos.json
git commit -m "Normalizar los 407 productos: precios enteros y slugs únicos"
```

---

### Tarea 3: Enriquecer los datos y validarlos

**Archivos:**
- Crear: `tools/enriquecer.py`, `tools/validar.py`, `tools/test_validar.py`, `data/schema.json`
- Modifica: `src/datos/productos.json`

**Interfaces:**
- Consume: `src/datos/productos.json` de la tarea 2.
- Produce: los campos `marca`, `presentacion`, `subcategoria`, `rx`, `origen`.
  `validar(productos) -> list[str]` devuelve la lista de errores; vacía si todo está bien.

- [ ] **Paso 1: escribir `tools/enriquecer.py`**

Deriva **solo lo que se lee literal del título** y lo marca con origen `"titulo"`:
presentación (`X 30 TAB`, `120 ML`, `X 60 CAPS`), miligramos (`500 MG`), y marca cuando
el título la trae al final entre las conocidas.

La subcategoría se deriva por diccionario de palabras clave y se marca `"inferido"`.

**`rx` arranca en `null` con origen `"pendiente"`, nunca inferido**, porque afirmar que un
medicamento de control no requiere fórmula es un problema legal. Se llena en revisión.

- [ ] **Paso 2: escribir la prueba del validador**

`tools/test_validar.py`:

```python
from validar import validar

def test_producto_correcto_no_da_errores():
    assert validar([{
        "slug": "abc", "titulo": "ABC", "precio": 1000, "precio_antes": None,
        "descuento": None, "categoria": "medicamentos", "imagenes": ["a.webp"],
        "descripcion": "x", "stock": True,
    }]) == []

def test_precio_como_texto_es_error():
    errores = validar([{
        "slug": "abc", "titulo": "ABC", "precio": "$1.000",
        "categoria": "medicamentos", "imagenes": ["a.webp"],
    }])
    assert any("precio" in e for e in errores)

def test_slug_repetido_es_error():
    p = {"slug": "abc", "titulo": "A", "precio": 1, "categoria": "c", "imagenes": ["a.webp"]}
    assert any("repetido" in e for e in validar([p, dict(p)]))

def test_sin_imagenes_es_error():
    assert any("imagen" in e for e in validar([
        {"slug": "a", "titulo": "A", "precio": 1, "categoria": "c", "imagenes": []}]))
```

- [ ] **Paso 3: comprobar que falla, escribir `validar.py`, comprobar que pasa**

```bash
python3 -m pytest tools/test_validar.py -v
```

`validar.py` revisa: campos obligatorios presentes, `precio` entero positivo, `slug` único
y en minúsculas sin espacios, al menos una imagen, y que **cada archivo de imagen exista
en `public/img/`**. Devuelve mensajes con el slug del producto para poder ubicarlo.

- [ ] **Paso 4: correr el validador sobre los datos reales**

```bash
python3 tools/validar.py src/datos/productos.json
```

Esperado: `407 productos válidos` o la lista concreta de qué está mal.

- [ ] **Paso 5: commit**

```bash
git add tools/ data/schema.json src/datos/productos.json
git commit -m "Enriquecer datos con origen trazable y validador con esquema"
```

---

### Tarea 4: Imágenes

**Archivos:**
- Crear: `tools/preparar-imagenes.py`
- Produce: `public/img/*.webp`

- [ ] **Paso 1: copiar solo las imágenes referenciadas**

Las 1.265 imágenes de la carpeta heredada incluyen duplicados en `.jpg` y `.webp`. Copiar
únicamente las que aparecen en `productos.json`, en WebP, quitando el sufijo `-600x600`.

- [ ] **Paso 2: verificar que no falta ninguna**

```bash
python3 tools/validar.py src/datos/productos.json
du -sh public/img
```

Esperado: sin errores de imagen faltante, y un peso total por debajo de 20 MB.

- [ ] **Paso 3: commit**

---

### Tarea 5: Datos del negocio y utilidades compartidas

**Archivos:**
- Crear: `src/datos/config.json`, `src/datos/categorias.json`
- Crear: `src/scripts/formato.js`, `src/scripts/test-formato.mjs`

**Interfaces:**
- Produce: `pesos(n) -> string` (`62900` → `"$62.900"`), `sinTildes(s) -> string`.
  Los consumen el buscador, el carrito y las tarjetas.

- [ ] **Paso 1: `src/datos/config.json` con los datos reales**

```json
{
  "negocio": "Droguería Xivica",
  "whatsapp": "573013665076",
  "envio": { "gratis_desde": 60000, "minutos_min": 45, "minutos_max": 90 },
  "sedes": [
    { "nombre": "Villa del Prado", "direccion": "Cra 49B #171a-92",
      "telefono": "6013747807", "lat": 4.765, "lng": -74.045, "horario": "PENDIENTE" },
    { "nombre": "Tejares del Norte", "direccion": "Cra 49 #185-26 Local 1",
      "telefono": "3013665076", "lat": 4.772, "lng": -74.042, "horario": "PENDIENTE" }
  ],
  "legal": { "habilitacion": "PENDIENTE", "regente": "PENDIENTE" }
}
```

La tercera sede no se incluye hasta tener dirección real. Los `PENDIENTE` se renderizan
visibles en el sitio para que no se publiquen por descuido.

- [ ] **Paso 2: prueba de `formato.js`**

```js
import { pesos, sinTildes } from "./formato.js";
import assert from "node:assert";

assert.equal(pesos(62900), "$62.900");
assert.equal(pesos(8200), "$8.200");
assert.equal(pesos(0), "$0");
assert.equal(sinTildes("ACETAMINOFÉN"), "acetaminofen");
assert.equal(sinTildes("Bebé & Maternidad"), "bebe & maternidad");
console.log("formato.js correcto");
```

- [ ] **Paso 3: comprobar que falla, implementar, comprobar que pasa**

```bash
node src/scripts/test-formato.mjs
```

- [ ] **Paso 4: commit**

---

### Tarea 6: Estructura común — Layout, encabezado, subnav, pie

**Archivos:**
- Crear: `src/layouts/Base.astro`, `src/layouts/Tienda.astro`
- Crear: `src/components/{Header,SubnavCategorias,Footer,Logo}.astro`

**Interfaces:**
- Produce: `<Tienda titulo descripcion>` que envuelve toda página de la tienda.
  `Logo.astro` es el **único** lugar que referencia el archivo del logo.

- [ ] **Paso 1: `Logo.astro`, punto único de la marca**

```astro
---
const { alto = 40, clase = "" } = Astro.props;
const base = import.meta.env.BASE_URL;
---
<img src={`${base}img/logo-xivica.png`} alt="Droguería Xivica"
     height={alto} width={Math.round(alto * 160 / 74)} class={clase} />
```

- [ ] **Paso 2: `Base.astro` con meta, Open Graph y datos estructurados**

- [ ] **Paso 3: `Header.astro`** — logo, selector de sede, buscador central, favoritos,
  volver a comprar, carrito con contador. Todos los textos desde `config.json`.

- [ ] **Paso 4: `SubnavCategorias.astro`** — barra azul con las categorías desde
  `categorias.json`, "Mundo Ofertas" destacado en lima.

- [ ] **Paso 5: `Footer.astro`** — sedes, legales, habilitación sanitaria, redes.

- [ ] **Paso 6: verificar**

```bash
npm run build && npx astro preview --port 4321 &
sleep 3 && curl -s localhost:4321 | head -40
```

- [ ] **Paso 7: commit**

---

### Tarea 7: Tarjeta y grilla de productos

**Archivos:**
- Crear: `src/components/TarjetaProducto.astro`, `src/components/GrillaProductos.astro`

**Interfaces:**
- Consume: `pesos()` de la tarea 5.
- Produce: `<TarjetaProducto producto={p} prioridad={bool} />`. La usan la portada, el
  catálogo, las ofertas y los relacionados.

- [ ] **Paso 1: tarjeta según la dirección B** — imagen cuadrada, badge rojo de descuento,
  título a dos líneas, precio tachado arriba, precio grande, ahorro en lima, botón azul.
  `width` y `height` explícitos, `fetchpriority="high"` cuando `prioridad`.

- [ ] **Paso 2: grilla** de 5 columnas en escritorio, 3 en tableta, 2 en móvil.

- [ ] **Paso 3: verificar que no hay salto de layout** — todas las imágenes con dimensiones.

- [ ] **Paso 4: commit**

---

### Tarea 8: Portada

**Archivos:**
- Crear: `src/pages/index.astro`, `src/datos/home.json`
- Crear: `src/components/{BannerCarrusel,RailCategorias,BarraOfertas,FranjaGarantias}.astro`

- [ ] **Paso 1: `home.json`** con los textos de los tres banners y las garantías.
- [ ] **Paso 2: banner-carrusel** de 300 px, tres diapositivas, autoavance de 6 s, puntos.
  Se detiene al pasar el ratón y respeta `prefers-reduced-motion`.
- [ ] **Paso 3: rail de categorías** circulares con desplazamiento horizontal.
- [ ] **Paso 4: barra de ofertas** oscura con cuenta regresiva al cierre del día.
- [ ] **Paso 5: grilla de más vendidos en oferta** y franja de garantías.
- [ ] **Paso 6: verificar** que la portada compila y que las imágenes que faltan usan
  `placehold.co` con la medida correcta. Anotar cada una en `PENDIENTES.md`.
- [ ] **Paso 7: commit**

---

### Tarea 9: Las 407 páginas de producto

**Es la razón de usar Astro. Verificar el conteo, no darlo por hecho.**

**Archivos:**
- Crear: `src/pages/producto/[slug].astro`

- [ ] **Paso 1: `getStaticPaths` desde `productos.json`**

```astro
---
import productos from "../../datos/productos.json";
export function getStaticPaths() {
  return productos.map((producto) => ({ params: { slug: producto.slug }, props: { producto } }));
}
const { producto } = Astro.props;
---
```

- [ ] **Paso 2: galería con miniaturas, precio con ahorro, botón agregar, aviso de
  fórmula médica cuando `rx` sea verdadero, y cuatro relacionados de la misma categoría.**

- [ ] **Paso 3: datos estructurados `Product` con precio y disponibilidad**, que es lo que
  hace que Google muestre el precio en el resultado de búsqueda.

- [ ] **Paso 4: verificar el conteo real**

```bash
npm run build
ls dist/producto | wc -l
```

Esperado: **407**. Si sale menos, hay slugs colisionando y debe corregirse en la tarea 2.

- [ ] **Paso 5: commit**

---

### Tarea 10: Catálogo con filtros y buscador

**Archivos:**
- Crear: `src/pages/catalogo.astro`, `src/pages/categoria/[cat].astro`, `src/pages/ofertas.astro`
- Crear: `src/components/FiltrosCatalogo.astro`
- Crear: `src/scripts/filtros.js`, `src/scripts/buscador.js`, `src/scripts/test-buscador.mjs`

**Interfaces:**
- Consume: `sinTildes()` de la tarea 5.
- Produce: `buscar(indice, consulta) -> producto[]` ordenado por relevancia.

- [ ] **Paso 1: prueba del buscador**

```js
import { buscar } from "./buscador.js";
import assert from "node:assert";

const indice = [
  { titulo: "ACETAMINOFÉN 500 MG X 20 TAB", slug: "a", categoria: "medicamentos" },
  { titulo: "CREMA NIVEA BODY MILK", slug: "b", categoria: "cuidado-personal" },
];

// sin tildes encuentra con tildes
assert.equal(buscar(indice, "acetaminofen")[0].slug, "a");
// mayúsculas y minúsculas dan igual
assert.equal(buscar(indice, "NIVEA")[0].slug, "b");
// un error de tipeo todavía encuentra
assert.equal(buscar(indice, "acetaminofeno")[0].slug, "a");
// lo que no existe devuelve vacío
assert.deepEqual(buscar(indice, "zzzz"), []);
console.log("buscador correcto");
```

- [ ] **Paso 2: comprobar que falla, implementar, comprobar que pasa**

```bash
node src/scripts/test-buscador.mjs
```

- [ ] **Paso 3: filtros con estado en la URL** (`?cat=&marca=&min=&max=&oferta=&orden=`),
  para que el filtro sea compartible y el botón atrás funcione.

- [ ] **Paso 4: dropdown del buscador** con seis resultados y botón de agregar.

- [ ] **Paso 5: commit**

---

### Tarea 11: Carrito y cierre por WhatsApp

**Archivos:**
- Crear: `src/components/CarritoPanel.astro`
- Crear: `src/scripts/carrito.js`, `src/scripts/checkout.js`, `src/scripts/test-carrito.mjs`

**Interfaces:**
- Produce: `agregar(slug, cantidad)`, `quitar(slug)`, `total() -> int`,
  `mensajeWhatsApp(pedido) -> string`.

- [ ] **Paso 1: prueba del carrito y del mensaje**

```js
import { crearCarrito } from "./carrito.js";
import assert from "node:assert";

const c = crearCarrito({ persistir: false });
c.agregar({ slug: "a", titulo: "A", precio: 1000 }, 2);
c.agregar({ slug: "b", titulo: "B", precio: 500 }, 1);
assert.equal(c.total(), 2500);

// agregar dos veces el mismo suma cantidad, no duplica la línea
c.agregar({ slug: "a", titulo: "A", precio: 1000 }, 1);
assert.equal(c.lineas().length, 2);
assert.equal(c.total(), 3500);

c.quitar("a");
assert.equal(c.total(), 500);
console.log("carrito correcto");
```

- [ ] **Paso 2: comprobar que falla, implementar, comprobar que pasa**
- [ ] **Paso 3: persistencia en `localStorage`** envuelta en `try/catch`, porque en modo
  privado el acceso puede lanzar excepción.
- [ ] **Paso 4: panel del carrito** con total siempre visible y formulario de datos.
- [ ] **Paso 5: mensaje de WhatsApp formateado** con productos, cantidades, total,
  dirección y forma de pago.
- [ ] **Paso 6: commit**

---

### Tarea 12: Favoritos, volver a comprar y mapas

**Archivos:**
- Crear: `src/scripts/favoritos.js`, `src/scripts/historial.js`, `src/scripts/mapa.js`

- [ ] **Paso 1: favoritos** en `localStorage`, con corazón en la tarjeta.
- [ ] **Paso 2: historial** de pedidos enviados, para "volver a comprar".
- [ ] **Paso 3: Leaflet cargado solo al entrar el mapa en pantalla**, con
  `IntersectionObserver`. Un mapa para las sedes y otro para elegir la dirección de entrega.
- [ ] **Paso 4: commit**

---

### Tarea 13: Páginas de confianza y legales

**Archivos:**
- Crear: `src/pages/{sedes,servicios,nosotros,contacto,404}.astro`
- Crear: `src/pages/legal/{privacidad,terminos,datos}.astro`
- Crear: `src/datos/{servicios,legal,nosotros}.json`

- [ ] **Paso 1: sedes** con mapa, direcciones, teléfonos y horarios (marcados PENDIENTE).
- [ ] **Paso 2: servicios** — domicilio, fórmula médica, asesoría, recoger en tienda.
- [ ] **Paso 3: legales** — tratamiento de datos según la Ley 1581 de 2012, términos, y el
  aviso de que los medicamentos de control requieren fórmula médica.
- [ ] **Paso 4: 404** con buscador, que es lo útil en una tienda.
- [ ] **Paso 5: commit**

---

### Tarea 14: SEO y rendimiento

- [ ] **Paso 1: `sitemap.xml` y `robots.txt`** con las 407 fichas.
- [ ] **Paso 2: datos estructurados `LocalBusiness`** con las sedes.
- [ ] **Paso 3: medir con Lighthouse** y anotar el resultado real.

```bash
npm run build && npx astro preview --port 4321 &
sleep 3 && npx lighthouse http://localhost:4321 --only-categories=performance,accessibility \
  --preset=perf --chrome-flags="--headless" --output=json --output-path=/tmp/lh.json
python3 -c "
import json; r=json.load(open('/tmp/lh.json'))['categories']
print({k: round(v['score']*100) for k,v in r.items()})"
```

Objetivo: 90+ en rendimiento. **Anotar el número real obtenido, no el esperado.**

- [ ] **Paso 4: commit**

---

### Tarea 15: Publicación y blindaje del JSON

**Archivos:**
- Crear: `.github/workflows/validar.yml`, `.github/workflows/deploy.yml`

- [ ] **Paso 1: acción que valida el JSON en cada push.** Si falla, no se despliega.
- [ ] **Paso 2: acción de despliegue a GitHub Pages** con `PUBLIC_BASE=/xivica/`.
- [ ] **Paso 3: crear el repositorio y subir**

```bash
gh repo create Gestiona2/xivica --private --source=. --remote=origin --push
```

- [ ] **Paso 4: verificar que el sitio publicado carga** y que las rutas con `base`
  funcionan (no basta con que compile).

---

### Tarea 16: Documentación de entrega

**Archivos:**
- Crear: `conocimiento_generado/{README,SITIO,MARCA,STACK,SECCIONES,COMO-EDITAR,PUBLICAR,LIMITES,PENDIENTES}.md`
- Crear: `AGENTS.md`, `CLAUDE.md`, `TUTORIAL.md`, `PENDIENTES.md`, `README.md`

- [ ] **Paso 1:** rellenar `entrega/AGENTS.md.template` con los datos de Xivica.
- [ ] **Paso 2: `SECCIONES.md`**, el más importante: una entrada por sección con dónde
  vive, qué contiene, cuántos elementos aguanta y cómo se agrega uno.
- [ ] **Paso 3: `COMO-EDITAR.md`** con las recetas reales — cambiar un precio, agregar un
  producto, poner algo en oferta, cambiar el WhatsApp, agregar una sede.
- [ ] **Paso 4: verificar que no queda ningún `{{marcador}}` sin reemplazar.**
- [ ] **Paso 5: commit**

---

### Tarea 17: Registro en el generador

- [ ] **Paso 1:** registrar el sitio en `generador/paginas_en_proceso.md`.
- [ ] **Paso 2:** crear `generador/pendientes/web-xivica.md` **solo como puntero** — los
  pendientes reales viven en el repo del sitio, por la regla 3.
- [ ] **Paso 3:** anotar en `generador/conocimiento/lecciones.md` la lección de este
  proyecto: **un catálogo con muchos productos necesita una URL por producto**, y por qué
  el archivo único no sirve para comercio.
- [ ] **Paso 4:** correr `python3 herramientas/revisar-frontera.py` y confirmar que no
  quedó conocimiento de Xivica dentro del generador.
- [ ] **Paso 5: commit en ambos repos.**
