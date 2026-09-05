# Con qué está hecho y dónde está cada cosa

## Tecnologías

| Qué | Versión | Para qué |
|---|---|---|
| Astro | 7 | Genera las 427 páginas HTML |
| Tailwind CSS | 4 | Sistema de estilos, usado solo para los tokens de color |
| JavaScript | módulos ES | Buscador, carrito, filtros. Sin frameworks ni librerías |
| Leaflet | 1.9.4 | Mapa de las sedes. Se descarga solo al llegar a esa sección |
| Python | 3.12 | Herramientas locales. **No corre en el servidor** |

No hay React, ni Vue, ni jQuery. El sitio publicado es HTML, CSS, JavaScript e imágenes.

## Estructura

```
src/
├── datos/          TODO el contenido editable. Un archivo por página
├── pages/          Una página del sitio por archivo
├── components/     Piezas que se repiten (tarjeta, cabecera, pie)
├── layouts/        El armazón común de todas las páginas
├── scripts/        El JavaScript que corre en el navegador
└── styles/         Colores, tipografía y estilos

public/             Lo que se copia tal cual: imágenes y tipografía
tools/              Herramientas locales. NO se suben al servidor
conocimiento_generado/  Esta documentación
```

## Si quieres cambiar X, el archivo es Y

| Quiero cambiar | Archivo |
|---|---|
| Un precio, un producto, una oferta | `src/datos/productos.json` |
| El WhatsApp, una sede, el mínimo de envío gratis | `src/datos/config.json` |
| Los banners y textos de la portada | `src/datos/home.json` |
| Las categorías del menú | `src/datos/categorias.json` |
| Los servicios | `src/datos/servicios.json` |
| Los textos legales | `src/datos/legal.json` |
| La página Nosotros | `src/datos/nosotros.json` |
| Lo que la gente busca y no encuentra | `src/datos/sinonimos.json` |
| Los colores o la tipografía | `src/styles/global.css` |
| Cómo se ve una tarjeta de producto | `src/components/TarjetaProducto.astro` **y** `src/scripts/tarjeta.js` |
| El logo | `public/img/logo-xivica.png` y `src/components/Logo.astro` |
| Qué productos salen destacados | `src/scripts/destacados.js` |

## Comandos

```bash
npm run dev      # ver el sitio en tu computador
npm run build    # compilarlo
npm test         # correr las 53 pruebas
python3 tools/validar.py src/datos/productos.json public/img
```

## Las herramientas de tools/

Se ejecutan **en el computador de quien trabaja**, nunca en el servidor. El sitio
publicado no necesita Python.

| Herramienta | Qué hace |
|---|---|
| `validar.py` | Revisa que el catálogo esté bien antes de publicar |
| `revisar-css.py` | Comprueba que no se use un color que no existe |
| `normalizar.py` | Convirtió el catálogo viejo al formato nuevo. Ya se usó |
| `enriquecer.py` | Dedujo presentación, marca y tipo de cada producto. Ya se usó |
| `preparar-imagenes.py` | Copió y optimizó las fotos. Ya se usó |

## Rendimiento medido

Lighthouse en móvil, sobre el sitio compilado:

| | Portada | Ficha | Catálogo |
|---|---|---|---|
| Rendimiento | 100 | 100 | 99 |
| Accesibilidad | 100 | 100 | 100 |
| SEO | 100 | 100 | 100 |
| Buenas prácticas | 100 | 100 | 100 |

El HTML de la portada pesa 52 KB. El sitio anterior pesaba 227 KB antes de mostrar nada.
