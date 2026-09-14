# Pendientes de Droguería Xivica

Lo que falta para poder publicar en el dominio definitivo. Se va tachando a medida que
llegan los datos.

## Bloquean la publicación

- [ ] **Número de habilitación sanitaria.** Aparece resaltado en amarillo en el pie del
      sitio hasta que llegue. Se pone en `src/datos/config.json` → `legal.habilitacion`.
- [ ] **Regente de farmacia responsable** (nombre y tarjeta profesional).
      `config.json` → `legal.regente` y `legal.tarjeta_profesional`.
- [ ] **NIT de la droguería.** `config.json` → `legal.nit`.
- [ ] **Revisión de qué productos requieren fórmula médica.** Hoy los 407 están sin
      marcar. Mientras siga así, la regla que los mantiene fuera de la portada no protege
      nada. Ver `conocimiento_generado/REGLAS-DEL-CATALOGO.md`, reglas 2 y 3.
- [ ] **Derechos de uso de las fotos.** Las 669 imágenes vienen del sitio anterior, que
      las tomó de catálogos de proveedores. Confirmar antes de publicar.
- [ ] **Dominio definitivo.** Está decidido que será uno nuevo, sin definir cuál.

## Datos que faltan pero no bloquean

- [ ] **Horarios de cada sede.** `config.json` → `sedes[].horario`.
- [ ] **Correo de contacto.** `config.json` → `correo`.
- [ ] **Tercera sede.** El sitio anterior la anunciaba como "próximamente". No se incluyó
      porque no hay dirección real. Se agrega en `config.json` → `sedes`.
- [ ] **Redes sociales**, si existen. `config.json` → `redes`.

## Diseño e imágenes

- [x] ~~**Logo en vector.**~~ Aplicado el emblema oficial del Manual de Marca v2.0
      (`public/img/isotipo-xivica.svg`, 14/09/2026).
- [x] ~~**Manual de marca.**~~ Aplicado el v2.0: paleta, Manrope + Inter, tagline, tono,
      iconografía y orden de la portada. Ver `conocimiento_generado/MARCA.md`.
- [ ] **Archivo del logotipo (nombre).** El manual aprueba una versión horizontal (emblema +
      nombre) pero solo entregó el emblema. El nombre está compuesto con Manrope en
      `src/components/Logo.astro`. Cuando llegue el archivo oficial, se reemplaza ahí.
- [ ] **Fotografías para el carrusel.** Hoy las piezas se dibujan con el círculo y la curva
      del logo, sin fotos. El manual pide personas reales, luz natural y fondos simples
      (cap. 33). Cuando existan, van en `src/datos/home.json` → `banners[].imagen`.
- [ ] **Fotos de las sedes y del equipo**, para las páginas de sedes y nosotros.

## Contradicciones entre los archivos del cliente

Hay que resolverlas con el cliente. El sitio sigue el **Manual v2.0**, que es el marcado
como definitivo.

- [ ] **La lámina `identidad visual.png` no coincide con el manual v2.0.** Usa Poppins y
      Montserrat (el manual: Manrope e Inter), otros colores (`#007CC3`, `#16A34A`,
      `#FACC15`), otro eslogan ("Tu salud, siempre cerca"; el manual: "Cerca cuando la
      necesitas") y **otro WhatsApp: 322 863 6554**, cuando el sitio usa el 301 366 5076.
      Confirmar cuál es el número vigente: es lo más delicado de los cuatro.
- [ ] **El manual dice 3 puntos de venta; solo hay dirección de dos.** Los textos del sitio
      ya no dicen "dos sedes". Falta la dirección, el teléfono y el horario del tercero.
- [ ] **El logo maestro y la tabla de colores difieren un poco.** El SVG trae `#03863E`,
      `#FDD603` y `#8AC840`; la tabla del manual, `#00813F`, `#FFD400` y `#84CF3B`. El logo se
      usa tal cual (el manual prohíbe tocarlo) y la interfaz usa los de la tabla. La
      diferencia no se nota a simple vista, pero conviene que el diseñador lo unifique.
- [ ] **El manual pide "texto blanco sobre azul", y sobre el azul oficial no se puede leer**
      (2,58:1). Se resolvió con un azul más oscuro del mismo matiz. Si el diseñador quiere
      sostener la regla, la solución es que el manual incluya ese azul de trabajo.

## Riesgos conocidos

- [ ] **El mapa depende de OpenStreetMap.** Las imágenes del mapa las sirve un
      proyecto sin ánimo de lucro cuya política de uso desaconseja el tráfico alto de
      sitios comerciales. En pruebas automatizadas algunas ya se rechazaron. Si el sitio
      crece, conviene pasar a un proveedor con plan gratuito generoso (MapTiler,
      Protomaps) o a una imagen estática del mapa. Mientras tanto, si el mapa no carga,
      las direcciones siguen escritas encima y los enlaces a Google Maps funcionan.

## Mejoras de datos

- [ ] **Galerías con fotos de otros productos.** Vienen así del sitio anterior. Ejemplo: la
      segunda foto del Oscillococcinum es una caja de Aciclovir. Hay que revisar las fotos
      adicionales producto por producto, o dejar solo la primera. Se editan en el campo
      `imagenes` de cada producto.
- [ ] **Nombres de producto en mayúsculas.** El manual pide evitar las mayúsculas
      excesivas. Los nombres vienen así del inventario (`ACETAMINOFEN 500 MG X 20 TAB`) y
      pasarlos a minúsculas a ciegas estropea marcas y siglas. Conviene hacerlo al
      revisar el catálogo, no automáticamente.

- [ ] **Subcategorías del 48% restante.** Se clasificó el 52% por palabras clave; el resto
      son genéricos que habría que revisar a mano para afinar los filtros.
- [ ] **Productos destacados.** Ninguno está marcado con `"destacado": true`, así que la
      portada se llena sola por ahorro. Cuando la droguería decida qué empujar, se marcan.
