# Marca de Droguería Xivica

## De dónde sale

**Manual de Marca v2.0 (2026)**, marcado como definitivo y aprobado. El original vive en
`insumos/manual de marca/`, que **no se sube** al repositorio porque contiene el brief del
propietario. Esta página resume solo lo que afecta al sitio web.

Si el manual cambia, se actualiza esta página y el bloque de colores de
`src/styles/global.css`. Nada más.

## Idea central

**Cerca cuando la necesitas.** Es el tagline oficial, y aparece en la portada, en el pie y en
la imagen que se ve al compartir el enlace. Se guarda en `src/datos/config.json` → `tagline`.

La marca debe sentirse cercana, confiable, profesional, moderna y resolutiva. **Nunca**
insegura, fría, arrogante, saturada ni oportunista.

## El logo

El logo oficial es el **emblema circular**: aro amarillo, campo azul, cruz blanca y hojas
verdes.

- **Archivo:** `public/img/isotipo-xivica.svg`, copia exacta del archivo maestro aprobado
  (`Drogueria_Xivica_logo_final_vector_fiel.svg`). **No se redibuja, no se recolorea, no se
  le ponen sombras ni degradados.** El manual lo prohíbe expresamente.
- **Lo usa un solo archivo:** `src/components/Logo.astro`. Cambiarlo ahí lo cambia en todo el
  sitio.
- **Favicon e ícono del celular:** el mismo isotipo (`isotipo-xivica.svg` y
  `isotipo-xivica-180.png`).
- **Tamaño mínimo:** isotipo de 32 px; logo completo de 120 px.

**El nombre junto al logo** ("Droguería" en verde, "Xivica" en azul) está compuesto con la
tipografía oficial, porque el manual aprueba la versión horizontal pero **no entregó el archivo
del logotipo**. Cuando llegue, se reemplaza en `Logo.astro`. Está en `PENDIENTES.md`.

## Colores

Todos viven en `src/styles/global.css`. **Ningún archivo escribe un color directamente.**

### Paleta oficial del manual

| Nombre en el manual | Variable | Color | Dónde se usa en el sitio |
|---|---|---|---|
| Azul Xivica | `--azul-marca` | `#00AAF9` | Barra de categorías, círculos decorativos |
| Amarillo Xivica | `--amarillo` | `#FDD603` | Franja superior, botones principales, etiquetas de descuento |
| Verde Xivica | `--verde` | `#03863E` | "Droguería" del logo, tagline, marcas de verificación |
| Verde lima Xivica | `--lima` | `#8AC840` | Solo acento. Nunca texto |

> Decisión del propietario (17/09/2026): los colores de la tabla del manual se
> unificaron con los del archivo del logo (`Drogueria_Xivica_logo_final_vector_fiel.svg`),
> que mandan. El verde sobre blanco da 4,68:1 y sigue sirviendo como texto.
| Neutro oscuro | `--tinta` | `#17324D` | Todo el texto y los titulares |
| Gris claro | `--bg-soft` | `#F4F7F9` | Fondos del pie, sedes y módulos |

### Tonos de trabajo, derivados para que se pueda leer

| Variable | Color | Para qué | Contraste |
|---|---|---|---|
| `--azul` | `#0070A8` | Botones con texto blanco, precios, enlaces | 5,41:1 |
| `--azul-hondo` | `#005580` | Fondo del carrusel, estados activos | 8,04:1 |
| `--verde-texto` | `#006D35` | "Ahorras $…" y "Domicilio gratis" | 5,78:1 |
| `--text-muted` | `#56657A` | Textos secundarios | 5,52:1 sobre el gris claro |
| `--error` | `#C62A1E` | Solo errores de formulario. No es color de marca | — |

### La regla que no se puede romper

**Los colores de la paleta oficial, salvo el verde y el neutro oscuro, no sirven como texto
pequeño.** Medidos sobre blanco: el azul da 2,58:1, el amarillo 1,43:1 y el verde lima
1,91:1. El mínimo para leer es 4,5:1.

El manual pide "texto blanco sobre azul", pero **el blanco sobre el azul oficial da 2,58:1**,
así que tampoco se puede leer en tamaños pequeños. Por eso:

- El **azul oficial** va de fondo con **texto oscuro** encima (5,08:1). Así está la barra de
  categorías.
- Donde hace falta **texto blanco sobre azul** (botones, carrusel), se usa `--azul` o
  `--azul-hondo`, que son el mismo matiz oscurecido.
- El **amarillo** va siempre de fondo, con `--tinta` encima (9,17:1). Nunca como letra.

Si se cambia un color, hay que volver a medir. El sitio tiene 100 de accesibilidad en todas
las páginas y esto es lo que la sostiene.

### Lo que salió de la paleta

El rojo de los descuentos, el verde lima viejo y el cian **no están en el manual** y se
quitaron. Los descuentos son ahora etiquetas amarillas.

## Tipografía

| Uso | Fuente | Archivo |
|---|---|---|
| Titulares, precios, botones de la barra | **Manrope** | `public/fonts/manrope-variable.woff2` |
| Texto, descripciones, formularios | **Inter** | `public/fonts/inter-variable.woff2` |

Las dos van guardadas dentro del sitio: no se descargan de Google, ni por privacidad ni por
depender de un servidor ajeno.

Manrope viene apretada de fábrica: **no añadirle interletrado negativo**, o las palabras
cortas se pegan.

## Formas y gráfica

Del manual, capítulos 30 y 31:

- **Esquinas suaves**, círculos y curvas. Sombras muy ligeras.
- **Recursos gráficos:** el círculo y la curva amarilla del logo. Se usan en el carrusel, en
  el cierre de la portada y en la imagen para compartir. No se copian literalmente en todas
  partes.
- **Iconos de línea**, redondeados y todos del mismo estilo. **Nada de emojis**: mezclan
  estilos.
- **Proporción aproximada:** mitad blanco, un tercio azul, pinceladas de amarillo y verde.

## Tono

Cercano, claro, profesional, humano y resolutivo.

**Sí:** "¿Necesitas encontrarlo? Estamos cerca para ayudarte." · "Escríbenos." · "Consulta
disponibilidad."
**No:** "¡LA MEJOR DROGUERÍA CON LOS PRECIOS MÁS BAJOS!"

**Nunca:** mayúsculas excesivas, urgencia artificial, alarmismo, promesas de curación ni
diagnósticos. Por eso **se quitó la cuenta regresiva** de las ofertas: el manual pide no
competir con mensajes de urgencia.

Llamados a la acción aprobados: *Escríbenos · Consulta disponibilidad · Pide el tuyo ·
Encuéntranos cerca · Habla con nuestro equipo · Estamos para ayudarte.*
