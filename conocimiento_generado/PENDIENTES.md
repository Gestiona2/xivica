# Pendientes de Droguería Xivica

Lo que falta para poder publicar en el dominio definitivo. Se va tachando a medida que
llegan los datos.

## Bloquean la publicación

- [x] ~~**Número de habilitación sanitaria.**~~ Confirmados por el propietario el
      16/09/2026: `MS00010200`, `MS00017993` y `MS00001129` en `config.json` → `sedes[]`.
- [x] ~~**Regente de farmacia responsable.**~~ Resuelto: no aplica. La droguería no
      comercializa medicamentos de control especial (confirmado por el propietario el
      16/09/2026). `config.json` → `legal.regente_aplica: false`. Los textos del sitio ya
      no mencionan al regente.
- [x] ~~**NIT de la droguería.**~~ Entregado por el propietario el 17/09/2026:
      `1019155493-3` en `config.json` → `legal.nit`. Ya se muestra en el pie.
- [ ] **Revisión de qué productos requieren fórmula médica.** Hoy los 407 están sin
      marcar. Mientras siga así, la regla que los mantiene fuera de la portada no protege
      nada. Ver `conocimiento_generado/REGLAS-DEL-CATALOGO.md`, reglas 2 y 3.
- [x] ~~**Derechos de uso de las fotos.**~~ Confirmado por el propietario el 17/09/2026:
      las imágenes que vienen del sitio anterior se pueden usar.
- [ ] **Dominio definitivo.** Decidido por el propietario el 17/09/2026:
      **drogueriaxivica.com**. El cambio se hace cuando todo esté listo y lo hace
      Gestiona2, no el cliente.

## Datos que faltan pero no bloquean

- [x] ~~**Correo de contacto.**~~ Entregado por el propietario el 17/09/2026:
      `ventas@drogueriacivica.com` en `config.json` → `correo`. Ya se muestra en
      la página de contacto.
- [x] ~~**Producto de la ventana emergente.**~~ Marcados por el propietario el
      17/09/2026 con `"promo_flash": true`: Acid Mantle loción x2, Centrum Silver
      Women 60 y Cerebrit 330 g + 50 g. Si se quita la marca de todos, la ventana
      no se muestra.
- [x] ~~**Horarios de cada sede.**~~ Confirmados por el propietario el 16/09/2026, iguales
      en las tres sedes: Lunes a sábado 7:30 a. m. – 9:30 p. m.; domingos y festivos
      9:00 a. m. – 9:00 p. m. Se editó `config.json` → `sedes[].horario`.
- [x] ~~**Tercera sede.**~~ Confirmada: **Verbenal**, Cra 11 #187-01, teléfono
      312 429 3060. Ya está publicada en `config.json` → `sedes`.
- [x] ~~**Redes sociales**, si existen.~~ Decidido por el propietario el 17/09/2026:
      no existen. No se muestran iconos hasta que existan las cuentas; en ese momento
      se agregan con su enlace. Poner iconos sin enlace confunde al que los toca.

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
- [x] ~~**El manual dice 3 puntos de venta; solo hay dirección de dos.**~~ Resuelto:
      la tercera sede es **Verbenal** (Cra 11 #187-01, 312 429 3060, mismos horarios),
      confirmada por el propietario el 16/09/2026. El sitio ya muestra las tres sedes.
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
- [x] ~~**Productos destacados.**~~ Marcados 8 de ejemplo el 17/09/2026 (pañales,
      bloqueadores, vitaminas, shampoo, tinte y loción de bebé: ninguno es medicamento,
      para no empujar medicinas a la portada). Cuando la droguería decida qué empujar,
      se cambian: ver `COMO-EDITAR.md`.
