# Cómo hacer los cambios más comunes

Cada receta dice qué archivo tocar y qué escribir. Después de cualquier cambio en el
catálogo, revisar con:

```
python3 tools/validar.py src/datos/productos.json public/img
```

---

## Cambiar el precio de un producto

En `src/datos/productos.json`, buscar el producto por su nombre y cambiar `precio`.

```json
"precio": 62900
```

**El precio va sin signo de pesos, sin puntos y sin comillas.** `62900`, no `"$62.900"`.
Si se escribe mal, el sitio no se publica.

---

## Poner un producto en oferta

Se agrega `precio_antes` con el precio de antes y `descuento` con el porcentaje:

```json
"precio": 32600,
"precio_antes": 44010,
"descuento": 26
```

`precio_antes` tiene que ser **mayor** que `precio`, o el sitio no se publica. El ahorro en
pesos lo calcula la página sola.

Para quitar la oferta, poner los dos en `null`:

```json
"precio_antes": null,
"descuento": null
```

---

## Agregar un producto nuevo

Copiar un producto parecido del archivo y cambiarle los datos. Los campos obligatorios son
`slug`, `titulo`, `precio`, `categoria` e `imagenes`.

```json
{
 "slug": "nombre-del-producto-en-minusculas-con-guiones",
 "titulo": "NOMBRE DEL PRODUCTO",
 "precio": 15000,
 "precio_antes": null,
 "descuento": null,
 "categoria": "medicamentos",
 "subcategoria": null,
 "marca": null,
 "presentacion": "500 mg · 20 Tabletas",
 "rx": null,
 "stock": true,
 "destacado": false,
 "imagenes": ["nombre-de-la-foto.webp"],
 "descripcion": "",
 "origen": { "rx": "pendiente" }
}
```

El `slug` es la dirección del producto en internet: tiene que ser **único**, en minúsculas,
sin tildes y con guiones en vez de espacios.

La foto debe estar guardada en `public/img/` con ese mismo nombre, o el sitio no se
publica.

---

## Destacar un producto en la portada

Poner `"destacado": true`. Aparecerá primero en la portada.

Los productos con `"rx": true` **no** salen destacados aunque se marquen: ver
`REGLAS-DEL-CATALOGO.md`.

---

## Marcar que un producto agotó

```json
"stock": false
```

---

## Cambiar el WhatsApp

En `src/datos/config.json`, dos campos:

```json
"whatsapp": "573013665076",
"whatsapp_visible": "301 366 5076"
```

El primero es el número con el código de país y sin espacios; es el que abre WhatsApp. El
segundo es el que se ve escrito. **Hay que cambiar los dos.**

---

## Agregar la tercera sede

En `src/datos/config.json`, dentro de `sedes`, agregar:

```json
{
  "id": "nombre-corto-sin-espacios",
  "nombre": "Nombre de la sede",
  "direccion": "Cra 00 #00-00",
  "telefono": "6011234567",
  "telefono_visible": "601 123 4567",
  "lat": 4.77,
  "lng": -74.04,
  "horario": "Lunes a sábado, 7:00 a 21:00"
}
```

`lat` y `lng` se sacan de Google Maps: clic derecho sobre el punto y copiar las
coordenadas. Aparece sola en el pie, en la página de sedes y en el mapa.

---

## Poner el horario de una sede

En `src/datos/config.json`, cambiar `"horario": "PENDIENTE"` por el horario real. Mientras
diga PENDIENTE, se muestra resaltado en amarillo en el sitio.

---

## Cambiar el mínimo para envío gratis

En `src/datos/config.json`:

```json
"envio": { "gratis_desde": 60000, ... }
```

Cambia solo en la franja de arriba, en el carrito y en la página de servicios.

---

## Cambiar los banners de la portada

En `src/datos/home.json`, dentro de `banners`. Cada uno tiene etiqueta, título, texto,
botón y a dónde lleva.

El título funciona mejor con menos de 60 caracteres; más largo se ve apretado en celular.

---

## Que el buscador encuentre algo que la gente escribe

Si alguien busca "pañales" y no encuentra nada porque los productos se llaman "WINNY", se
agrega en `src/datos/sinonimos.json`:

```json
"panales": ["winny", "pañal", "bebe"]
```

A la izquierda lo que escribe la gente, a la derecha lo que hay en los nombres de los
productos.

---

## Cambiar un color de todo el sitio

En `src/styles/global.css`, en el bloque de arriba. **Antes de cambiar un color, leer la
regla de contraste en `MARCA.md`**: el lima y el cian no sirven como letra sobre fondo
claro.
