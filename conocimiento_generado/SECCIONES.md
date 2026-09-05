# Inventario de secciones

Una entrada por cada sección editable del sitio: dónde vive, qué contiene, cuánto aguanta
y cómo se agrega un elemento.

---

## Franja superior (todas las páginas)

- **Cómo se llama para el cliente:** "la barra verde de arriba"
- **Dónde está:** `src/datos/config.json` → `envio` y `whatsapp_visible`
- **Qué muestra:** envío gratis desde, tiempo de entrega y el WhatsApp
- **Límite:** en celular se ocultan el tiempo de entrega y las sedes por falta de espacio.
  No agregar más textos aquí.

---

## Buscador (todas las páginas)

- **Cómo se llama:** "el buscador"
- **Dónde está:** el texto de ejemplo en `src/components/Header.astro`
- **Qué encuentra:** nombre, marca, categoría, tipo y presentación de los 407 productos
- **Muestra:** 6 resultados. Más no caben sin tapar la página.
- **Aguanta:** que se escriba sin tildes, en minúsculas y con una errata
- **Para que encuentre algo que no encuentra:** agregar la palabra en
  `src/datos/sinonimos.json`

---

## Barra de categorías (todas las páginas)

- **Cómo se llama:** "el menú azul"
- **Dónde está:** `src/datos/categorias.json`
- **Cuántas caben bien:** 7 a 9. Con más, en computador ya no caben y hay que desplazar.
- **Cómo se agrega una:** un objeto con `id`, `nombre`, `icono` y `orden`. El `id` tiene
  que coincidir con la `categoria` de los productos, o la página saldrá vacía.

---

## Carrusel de la portada

- **Cómo se llama:** "los banners grandes de arriba"
- **Dónde está:** `src/datos/home.json` → `banners`
- **Cuántos caben bien:** 3 a 5. Con más, nadie llega al último.
- **Largo del título:** hasta 60 caracteres. Más largo se ve apretado en celular.
- **Largo del texto:** hasta 110 caracteres.
- **Imagen:** 520×300 px. **Hoy son marcadores grises** de placehold.co: las definitivas
  están pendientes de diseño.
- **Cómo se agrega uno:** un objeto con etiqueta, titulo, texto, boton, enlace e imagen.
- **Se mueve solo** cada 6 segundos, y se detiene al pasar el ratón.

---

## Accesos rápidos (portada)

- **Cómo se llama:** "los círculos de categorías"
- **Dónde está:** `src/datos/home.json` → `accesos`
- **Cuántos caben bien:** 6 a 10. En celular se desplazan de lado.
- **Texto:** una o dos palabras. Tres se ven apretadas.

---

## Barra de ofertas del día (portada y ofertas)

- **Cómo se llama:** "la barra negra con el reloj"
- **Dónde está:** `src/components/BarraOfertas.astro`
- **La cuenta regresiva** va hasta la medianoche del día, y la calcula el navegador de cada
  persona con su propia hora.

---

## Filas de productos (portada)

- **Cómo se llama:** "los productos de la portada"
- **Dónde está:** `src/pages/index.astro`, y el criterio en `src/scripts/destacados.js`
- **Cuántos muestra:** 10 en ofertas y 5 por categoría
- **Cómo se decide cuáles:** ver `REGLAS-DEL-CATALOGO.md`, regla 1
- **Para empujar un producto:** ponerle `"destacado": true` en el catálogo

---

## Tarjeta de producto (en todas las listas)

- **Dónde está:** `src/components/TarjetaProducto.astro`
- **Muestra:** foto, descuento, marca, nombre a dos líneas, presentación, precio, ahorro y
  botón de agregar
- **Cuidado:** existe una copia en JavaScript, `src/scripts/tarjeta.js`, para las listas que
  se pintan al filtrar. **Si se cambia una, hay que cambiar la otra.**

---

## Ficha de producto

- **Dónde está:** `src/pages/producto/[slug].astro`. Se genera una por producto.
- **Muestra:** galería, precio con ahorro, aviso de fórmula si aplica, botón de agregar,
  ventajas, descripción y 5 relacionados de la misma categoría
- **Descripción:** hasta unos 400 caracteres se ve bien. Se edita en el campo `descripcion`
  del producto. **Nunca escribir indicaciones médicas ahí.**

---

## Catálogo con filtros

- **Dónde está:** `src/pages/catalogo.astro`
- **Filtra por:** categoría, precio, marca (42 disponibles), tipo (26) y dos casillas
- **Ordena por:** relevancia, menor precio, mayor precio, mayor descuento y nombre
- **Muestra de a 24** productos, con un botón para ver más
- **Los filtros quedan en la dirección**, así que se pueden compartir por WhatsApp

---

## Carrito

- **Cómo se llama:** "el carrito"
- **Dónde está:** `src/components/` dentro del layout, y `src/scripts/carrito.js`
- **Formulario:** nombre, teléfono y dirección son obligatorios; barrio, forma de pago y
  nota son opcionales
- **Formas de pago:** se editan en `src/scripts/carrito.js`, buscando "Efectivo"
- **Al enviar** abre WhatsApp con el pedido escrito. No cobra nada en línea.

---

## Pie de página

- **Dónde está:** `src/components/Footer.astro`, con los datos de `config.json`
- **Muestra:** logo, categorías, enlaces, sedes, datos legales y el aviso de fórmula médica
- **Lo que falta se ve resaltado en amarillo.** Es a propósito.

---

## Servicios

- **Dónde está:** `src/datos/servicios.json`
- **Cuántos caben bien:** 3 a 6
- **Cada uno tiene:** título, resumen de una línea, párrafo de detalle y 3 puntos
- **Puntos:** 2 a 4 por servicio. Más de 4 se lee como lista de supermercado.

---

## Sedes

- **Dónde está:** `src/datos/config.json` → `sedes`
- **Cuántas caben bien:** 2 a 6, en tarjetas que se acomodan solas
- **El mapa** se dibuja con las coordenadas de cada sede y se carga solo al llegar ahí

---

## Legales

- **Dónde está:** `src/datos/legal.json`
- **Tres documentos:** privacidad, tratamiento de datos y términos
- **Cada uno** es una lista de secciones con título y texto
- **Al cambiar algo**, actualizar también la fecha en `actualizado`
