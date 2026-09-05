# Marca de Droguería Xivica

## Estado

**No hay manual de marca todavía.** Los colores salieron del logo existente, tomados con
cuentagotas. Cuando exista el manual, se aplica cambiando un solo bloque de
`src/styles/global.css`.

## El logo

`public/img/logo-xivica.png`, un PNG de 160×74 píxeles que viene del sitio anterior.

Lo usa **un solo archivo**: `src/components/Logo.astro`. Cambiar el logo es reemplazar la
imagen y esa línea; aparece corregido en todo el sitio a la vez.

**Se ve borroso en pantallas de alta densidad**, porque es muy pequeño. Reemplazarlo por
un vector está en `PENDIENTES.md`.

El logo dice DROGUERÍA en verde lima, con la O convertida en un globo con una cruz blanca
de farmacia, y Xivica en blanco sobre un brochazo azul.

## Colores

Todos viven en `src/styles/global.css`. **Ningún archivo escribe un color directamente.**

| Nombre | Color | Dónde se usa |
|---|---|---|
| `--azul` | `#0b4da2` | Barra de categorías, botones, precios, enlaces |
| `--azul-hondo` | `#08356f` | Fondos oscuros y estados activos |
| `--cian` | `#00a0e0` | Degradados de los banners |
| `--cian-texto` | `#007cad` | El cian **cuando es texto** (ver abajo) |
| `--lima` | `#a0c030` | Franja superior, botón de buscar, etiquetas de ahorro |
| `--lima-tinta` | `#16300a` | El único color de texto que va **encima** del lima |
| `--tinta` | `#16202b` | Texto principal y la barra de ofertas |
| `--rojo-hondo` | `#c62a1e` | Solo las etiquetas de descuento |

### La regla que no se puede romper

**El lima y el cian de marca no sirven como texto sobre fondo claro.** El lima da 2,08:1 y
el cian 2,96:1 de contraste, cuando el mínimo legible es 4,5:1.

- El **lima** va siempre de fondo, con `--lima-tinta` encima. Nunca como letra sobre blanco.
- El **cian** como letra se usa en su versión `--cian-texto`, que sí cumple.

Si se cambian estos colores, hay que volver a comprobar el contraste. Es lo que llevó la
accesibilidad del sitio de 80 a 100.

## Tipografía

**Archivo**, en una sola familia para títulos y texto. El archivo está guardado en
`public/fonts/archivo-variable.woff2`, dentro del sitio: no se descarga de Google, ni por
privacidad ni por depender de un servidor ajeno.

## Tono

Directo y sin adornos. La gente entra a resolver algo concreto.

**Sí:** "Tu pedido llega en 45 a 90 minutos", "Ahorras $22.015", "Falta el horario".
**No:** "Somos líderes en salud y bienestar", "la mejor experiencia farmacéutica".

Nunca se promete lo que no se puede cumplir, ni se escriben indicaciones médicas.
