# Punto de partida — Astro + Tailwind

Base para todo sitio nuevo. Se copia entera a la carpeta del cliente y se llena; **no se
empieza desde una página en blanco.**

## Qué trae resuelto

- **Tokens de marca** con tema claro y oscuro, sin parpadeo al cargar
- **Botones, tarjetas, superficies de vidrio** y tipografía utilitaria
- **Apariciones al bajar** con GSAP y con CSS puro, respetando a quien pidió menos
  movimiento
- **Menú, pie, botón de tema, WhatsApp flotante, volver arriba**
- **Contadores animados** de cifras
- La estructura de `src/datos/` con el contenido separado del diseño

Todo probado en producción en emp2web.com. Los valores de marca vienen vacíos a propósito.

## La regla que sostiene todo esto

> **En los `.astro` no se escribe texto. Todo el contenido va en `src/datos/`.**

Los `.astro` definen **cómo se ve**; los JSON definen **qué dice**. Esto es lo que permite
que el cliente edite su sitio sin poder romper el diseño, y lo que hace que
`SECCIONES.md` se escriba casi solo.

Cuesta un paso más al construir. Se acepta: quien edita después no es quien construyó.

## Estructura

```
src/
  datos/
    sitio.json        → lo que se repite en todas las páginas (menú, pie, contacto)
    inicio.json       → contenido de la página de inicio
    <pagina>.json     → un archivo por página
  styles/global.css   → tokens, base y estilos del sitio
  layouts/Layout.astro→ lo común a todas las páginas
  pages/              → una página por ruta, leyendo de datos/
public/
  brand/              → logo, favicon
  img/                → fotos del negocio
  fonts/              → tipografías (.woff2)
  vendor/             → gsap/ y lucide/
```

## Pasos para arrancar un sitio

1. Copiar esta carpeta al proyecto del cliente.
2. Llenar `docs/MARCA.md` **antes** de tocar código.
3. Poner los cinco colores y las dos tipografías en el bloque `@theme` de `global.css`.
   Verificar el contraste en tema claro **y** oscuro.
4. Descargar las tipografías (variables, subset latin) a `public/fonts/` y GSAP + Lucide a
   `public/vendor/`. **No enlazar a servidores ajenos** — ver
   `conocimiento/politicas.md`.
5. Llenar `src/datos/sitio.json` con los datos del negocio.
6. Llenar `src/datos/inicio.json` sección por sección.
7. Escribir los estilos propios de cada sección al final de `global.css`, siempre con las
   variables semánticas (`var(--text)`, `var(--bg)`), nunca con colores a mano.
8. Ir escribiendo `conocimiento_generado/` **a medida que se construye**, no al final.

## Cosas que se rompen fácil

- **Colores escritos a mano** en vez de variables → el tema oscuro se ve mal.
- **Texto dentro del `.astro`** → el agente del cliente no lo encuentra y lo duplica.
- **Quitar `prefers-reduced-motion`** → problema de accesibilidad, no de estética.
- **Probar solo en el editor** → hay que abrirlo en 320px y 375px reales.
