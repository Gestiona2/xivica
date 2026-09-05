# Especificación — Droguería Xivica, sitio nuevo

> Fecha: 2026-09-04 · Estado: aprobado para implementación
> Reemplaza el sitio actual de un solo archivo (`drogueria/index.html`, 227 KB)

## 1. Qué se construye y por qué

Droguería Xivica es una droguería de barrio en el norte de Bogotá (Suba) con dos sedes
operando y una tercera por definir. Vende medicamentos, cuidado personal, productos de
bebé y suplementos. El pedido se toma y se cierra por WhatsApp, y se entrega a domicilio
en 45 a 90 minutos.

Hoy tiene una web funcional pero construida como un archivo HTML único de 227 KB con los
407 productos incrustados dentro del HTML. Funciona, pero tiene tres límites que este
proyecto resuelve:

1. **Un solo archivo no se puede mantener a cuatro manos.** El agente que edite productos
   y la persona que ajuste el diseño trabajan sobre el mismo archivo gigante.
2. **Una sola URL para 407 productos.** La ficha vive en `#p-<slug>`, así que Google
   indexa una página, no cuatrocientas. Para un comercio que compite por búsquedas de
   producto, eso es perder el canal principal de captación.
3. **El HTML pesa antes de mostrar nada**, porque arrastra el catálogo completo aunque el
   visitante solo vea la portada.

**El objetivo del sitio** es que alguien que busca un medicamento en Google llegue a la
ficha de ese medicamento, vea el precio, y termine el pedido por WhatsApp en menos de un
minuto.

## 2. Decisiones tomadas

| Decisión | Elección | Consecuencia |
|---|---|---|
| Framework | Astro | 407 páginas de producto reales, componentes sin duplicar |
| Marca | Xivica, identidad nueva | Se conservan datos reales; el logo actual se respeta por ahora |
| Dirección visual | **B — Mercado** | Retail denso inspirado en Farmatodo, referencia del dueño |
| Datos | JSON versionado en Git | Sin base de datos; historial y reversión por commit |
| Enriquecimiento | Derivado con IA, marcado por origen | Habilita filtros reales, auditable antes de publicar |
| Checkout | Solo WhatsApp | Cero comisiones, es como ya opera el negocio |
| Demo | GitHub Pages en `Gestiona2.github.io/xivica` | Requiere `base` configurable |
| Producción | Por definir con el cliente | No se ata el código a ninguna plataforma |
| Dominio | Nuevo, por definir | El actual `drogueriaxivica.com.co` no se reutiliza |

### Lo que se descartó, y por qué

- **Supabase.** Para servir el catálogo es más lento que un archivo estático y añade una
  dependencia externa en el camino crítico. Queda reservado para una eventual fase 2: un
  panel de administración que *genere* el JSON, no que lo reemplace. Por eso el modelo de
  datos usa nombres y tipos que mapean uno a uno a una tabla de Postgres.
- **HTML plano sin build.** Se evaluó a fondo. Pierde las 407 URLs indexables y obliga a
  duplicar el encabezado en doce páginas.
- **Pago en línea.** El negocio cobra contra entrega. Agregarlo sería resolver un problema
  que el cliente no tiene.

## 3. Arquitectura

```
web-xivica/
├── astro.config.mjs          base configurable por variable de entorno
├── package.json
├── src/
│   ├── layouts/
│   │   ├── Base.astro         head, meta, esquemas, carga de fuentes
│   │   └── Tienda.astro       Base + encabezado + subnav + pie + carrito
│   ├── components/
│   │   ├── Header.astro       logo, selector de sede, buscador, acciones
│   │   ├── SubnavCategorias.astro
│   │   ├── BannerCarrusel.astro
│   │   ├── RailCategorias.astro
│   │   ├── BarraOfertas.astro      con cuenta regresiva
│   │   ├── TarjetaProducto.astro
│   │   ├── GrillaProductos.astro
│   │   ├── FiltrosCatalogo.astro
│   │   ├── FranjaGarantias.astro
│   │   ├── CarritoPanel.astro
│   │   ├── BuscadorDropdown.astro
│   │   └── Footer.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── catalogo.astro
│   │   ├── producto/[slug].astro     ← genera 407 páginas
│   │   ├── categoria/[cat].astro     ← genera una por categoría
│   │   ├── ofertas.astro
│   │   ├── sedes.astro
│   │   ├── servicios.astro
│   │   ├── nosotros.astro
│   │   ├── contacto.astro
│   │   ├── 404.astro
│   │   └── legal/{privacidad,terminos,datos}.astro
│   ├── datos/                 ← TODO el contenido editable vive aquí
│   │   ├── productos.json     407 productos, fuente de verdad
│   │   ├── categorias.json
│   │   ├── config.json        WhatsApp, sedes, horarios, envío
│   │   ├── home.json          textos de la portada y banners
│   │   ├── servicios.json
│   │   └── legal.json
│   ├── scripts/               JS de cliente, ES modules
│   │   ├── carrito.js  buscador.js  filtros.js
│   │   ├── favoritos.js  historial.js  checkout.js  mapa.js
│   └── estilos/
│       ├── tokens.css  base.css  componentes.css
├── public/img/                imágenes optimizadas
├── tools/                     NO se sube a producción
│   ├── enriquecer.py  optimizar-img.py  validar.py
├── conocimiento_generado/     los 9 archivos de la entrega
├── AGENTS.md · CLAUDE.md · TUTORIAL.md · PENDIENTES.md · README.md
└── .github/workflows/validar.yml
```

**Regla estructural:** ningún `.astro` lleva texto escrito directamente. Todo el contenido
editable vive en `src/datos/`, un archivo por página. Es la regla 8 del generador y es lo
que permite que el agente del cliente edite sin tocar componentes.

## 4. Modelo de datos

### `productos.json` — una entrada por producto

```json
{
  "slug": "oscillococcinum",
  "titulo": "OSCILLOCOCCINUM",
  "precio": 62900,
  "precio_antes": 84915,
  "categoria": "medicamentos",
  "subcategoria": "antigripales",
  "marca": "Boiron",
  "presentacion": "30 dosis",
  "rx": false,
  "stock": true,
  "imagenes": ["100025268_10.webp", "7702605100132-1.webp"],
  "descripcion": "…",
  "origen": { "marca": "titulo", "subcategoria": "inferido", "rx": "revisado" }
}
```

Tres cambios frente al JSON actual, y los tres importan:

- **Los precios son números, no cadenas.** Hoy son `"$62,900.00"`, lo que obliga a
  desarmar el texto para poder ordenar o filtrar por precio, y hace imposible sumar sin
  errores de redondeo. Pasan a enteros en pesos. El formateo a `$62.900` se hace al
  mostrar, con `Intl.NumberFormat('es-CO')`.
- **El campo `origen`** dice de dónde salió cada dato derivado: `titulo` (leído literal),
  `inferido` (deducido por IA) o `revisado` (confirmado por una persona). Sin esto no hay
  forma de auditar 407 productos.
- **`rx`** marca si requiere fórmula médica. Arranca en `inferido` y **debe pasar a
  `revisado` por el regente de farmacia antes de publicar en producción.**

### `config.json` — los datos del negocio en un solo lugar

WhatsApp (`573013665076`), las tres sedes con dirección, teléfono, coordenadas y horario,
el mínimo de envío gratis ($60.000), y el rango de entrega (45–90 min).

## 5. Diseño — dirección B, "Mercado"

Colores tomados con cuentagotas del logo actual:

| Token | Valor | Uso |
|---|---|---|
| `--azul` | `#0b4da2` | Subnav, botones primarios, precios |
| `--azul-hondo` | `#08356f` | Fondos oscuros |
| `--cian` | `#00a0e0` | Degradados, acentos |
| `--lima` | `#a0c030` | Franja superior, estados activos, ahorro |
| `--tinta` | `#16202b` | Texto |

**El lima nunca se usa como texto pequeño sobre fondo claro**: no alcanza contraste AA.
Va como fondo con texto oscuro encima, o en piezas grandes.

Tipografía **Archivo** para todo, con `system-ui` de respaldo. Ancho de contenido 1320 px.
Grilla de productos de 5 columnas en escritorio, 3 en tableta, 2 en móvil.

Piezas propias de esta dirección: banner-carrusel de 300 px, rail de categorías
circulares, barra oscura de "Ofertas del día" con cuenta regresiva, tarjetas compactas con
precio tachado y ahorro en lima, franja de garantías al pie.

**Imágenes que no existen** (banners, fachadas de sedes, foto de equipo) van con
`placehold.co` a la medida correcta desde el primer momento, y cada una queda anotada en
`PENDIENTES.md`.

## 6. Funcionalidad

- **Buscador.** Índice normalizado sin tildes ni mayúsculas, tolerante a un error de
  tipeo. Dropdown con seis resultados y botón de agregar sin salir de la página.
- **Filtros.** Categoría, subcategoría, marca, rango de precio, solo ofertas, sin fórmula.
  El estado va en la URL, así que el filtro es compartible y el botón atrás funciona.
- **Carrito** en `localStorage`, se recupera al volver. Total siempre visible.
- **Favoritos** y **volver a comprar**, ambos locales al navegador.
- **Fórmula médica:** abre WhatsApp con un mensaje predefinido para enviar la foto.
- **Checkout:** formulario con nombre, teléfono, dirección con mapa, forma de pago y nota
  → mensaje de WhatsApp formateado.

## 7. Rendimiento y accesibilidad

Astro genera el HTML completo en el build, así que no hay parpadeo esperando datos. Las
imágenes llevan `width` y `height` para no saltar el layout, `fetchpriority="high"` en las
primeras y carga diferida en el resto. Leaflet solo se carga cuando el mapa entra en
pantalla.

Objetivo: Lighthouse móvil 90+ en portada y ficha.

Accesibilidad: contraste AA verificado, navegación completa por teclado, foco visible,
`prefers-reduced-motion` respetado, etiquetas en todos los controles.

## 8. Publicación

```
edición → push a GitHub → build en la nube → publicado
```

Nadie compila en su computador. Las ramas generan vistas previas para que el dueño apruebe
desde el celular antes de que salga a producción.

`astro.config.mjs` lee `PUBLIC_BASE` del entorno: `/xivica/` para el demo en GitHub Pages,
`/` para el dominio propio. Mudarlo es cambiar una variable, no reescribir rutas.

**Blindaje, porque un agente escribe el JSON:** `tools/validar.py` verifica el archivo
contra un esquema, y una GitHub Action lo corre en cada push. Si el JSON está mal, el
deploy no sale y producción nunca se rompe.

## 9. Entrega

Los nueve archivos de `conocimiento_generado/` (SITIO, MARCA, STACK, SECCIONES,
COMO-EDITAR, PUBLICAR, LIMITES, PENDIENTES, README), más `AGENTS.md` y `CLAUDE.md` en la
raíz, `TUTORIAL.md` con ejemplos reales de este sitio, y los scripts de instalación.

Se escriben **mientras se construye**, no al final.

## 10. Lo que falta y no se inventa

Estos datos no se pueden deducir y quedan marcados como pendientes visibles en el HTML
hasta que el cliente los entregue:

- Número de habilitación sanitaria / registro para el pie de página.
- Nombre y tarjeta profesional del regente de farmacia responsable.
- Horarios reales de cada sede.
- Dirección de la tercera sede, si ya existe.
- Revisión del campo `rx` por el regente.
- Dominio definitivo.
- Fotos propias de las sedes y del equipo.
