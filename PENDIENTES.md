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

- [ ] **Logo en vector.** El actual es un PNG de 160×74 píxeles que se ve borroso en
      pantallas de alta densidad. Se cambia en `public/img/logo-xivica.png` y en
      `src/components/Logo.astro`, que es el único sitio del código que lo referencia.
- [ ] **Manual de marca.** Decidido hacerlo después de ver el sitio funcionando. Los
      colores están centralizados en `src/styles/global.css`, así que aplicarlo será
      cambiar ese bloque.
- [ ] **Tres banners de portada.** Hoy son marcadores grises de `placehold.co`, en
      520×300. Los textos ya están escritos en `src/datos/home.json`.
- [ ] **Fotos de las sedes y del equipo**, para las páginas de sedes y nosotros.

## Mejoras de datos

- [ ] **Subcategorías del 48% restante.** Se clasificó el 52% por palabras clave; el resto
      son genéricos que habría que revisar a mano para afinar los filtros.
- [ ] **Productos destacados.** Ninguno está marcado con `"destacado": true`, así que la
      portada se llena sola por ahorro. Cuando la droguería decida qué empujar, se marcan.
