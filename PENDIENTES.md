# Pendientes de Droguería Xivica

Actualizado el 21/09/2026, comprobando cada punto contra `src/datos/` y no de memoria. Lo
tachado ya está resuelto y queda como registro de cómo se resolvió.

## Ya resuelto

- [x] ~~Habilitación sanitaria~~ — una por sede: MS00010200, MS00017993 y MS00001129.
- [x] ~~Regente de farmacia~~ — **no aplica**: la droguería no vende medicamentos de control
      especial (confirmado por el propietario el 16/09). Ver el punto 1 de "Bloquean" por el
      efecto que esto tiene sobre el campo de fórmula médica.
- [x] ~~NIT~~ — cargado; su dígito de verificación cuadra.
- [x] ~~Horarios y tercera sede (Verbenal)~~ — cargados. Las coordenadas de las tres siguen
      por confirmar (ver "Confirmar").
- [x] ~~Manual de marca y logo en vector~~ — aplicado el v2.0.
- [x] ~~"Otro número de WhatsApp" de la lámina de identidad~~ — era el de Tejares del Norte.
- [x] ~~Fotos de una sede~~ — llegaron 7 fotos de **Villa del Prado** (21/09). Usadas 5 en la
      portada, Sedes y Nosotros. Las otras dos son repetidas de la fachada.

## Bloquean la publicación en el dominio definitivo

1. **¿Quién confirma qué productos requieren fórmula médica?** Hoy los 407 están sin marcar
   (`rx` vacío) y la regla que mantiene esos productos fuera de la portada no protege nada.
   **`AGENTS.md` sigue diciendo que lo decide "el regente", y ya no hay regente.** El agente
   del cliente no tiene a quién obedecer en ese punto. Decisión del propietario: quién lo
   confirma (¿él mismo?), y revisar con él la lista. Ojo: "no vendemos medicamentos de control"
   no significa "ninguno requiere fórmula": un antibiótico la requiere aunque no sea de control.
2. **Definir la "zona cercana" del domicilio gratis.** Los términos (`/legal/domicilios`) dicen
   que en la zona cercana el domicilio es gratis "sin importar el valor del pedido", pero no
   dicen cuál es esa zona. Sin eso, cualquier cliente puede reclamar. Falta: barrios o radio
   por sede.
3. **Revisión de un abogado** de los cuatro textos legales (privacidad, tratamiento de datos,
   términos, domicilios). Están redactados con la Ley 1581 de 2012 como guía, **no son
   asesoría jurídica**.
4. **Derechos de uso de las fotos de producto.** Las 669 vienen del sitio anterior, que las
   tomó de catálogos de proveedores.
5. **Dominio y hosting definitivos.** Está decidido que será un dominio nuevo, sin definir.

## Confirmar con el cliente (datos que pueden estar mal)

- **Correo: `ventas@drogueria`*c*`ivica.com`**, con C, no con X. Puede ser el dominio real o
  un error de digitación. Está en el pie y en Contacto.
- **Teléfono de Tejares del Norte.** El mensaje del cliente dice 322 863 66**5**4 y la lámina
  hecha con IA dice 322 863 65**5**4: cambia un dígito. Se cargó el del mensaje.
- **Ubicación exacta de las tres sedes.** Las coordenadas son estimadas (las de Verbenal
  aproximadas por barrio). El botón "Cómo llegar" abre Google Maps **en esas coordenadas**:
  podría mandar al cliente a una cuadra equivocada. Pedir a cada sede la ubicación compartida
  desde WhatsApp o Google Maps.
- **Que las fotos del interior son de Villa del Prado.** Se asumió porque se tomaron en 100
  segundos, junto a la fachada, y se ve la misma pared. Confirmar.
- **Autorización de la persona de la foto de portada.** Es un empleado, reconocible. Una imagen
  es un dato personal (Ley 1581): hace falta su autorización, idealmente por escrito.
- **Los 8 productos destacados** son de ejemplo (así lo dice el commit que los marcó). El
  dueño debe elegir cuáles quiere empujar.
- **Servicios que se ven en las fotos y el sitio no menciona:** "Corresponsal bancario
  Bancolombia" y "Afiliada a Coopidrogas". Si son servicios vigentes, son un motivo más para
  visitar la sede. Confirmar antes de publicarlos.

## Falta material

- [ ] **Fotos de Tejares del Norte y Verbenal** (fachada e interior). En Sedes salen como
      "Foto de la sede próximamente". Se preparan con `tools/preparar_fotos.py`.
- [ ] **Fotos del equipo**, con autorización. El manual pide personas reales (cap. 33).
- [ ] **Fotos para los banners 2 y 3 del carrusel** (domicilio y fórmula médica). Hoy llevan
      icono. Una foto del domiciliario en moto serviría para el primero.
- [ ] **Perfiles de redes sociales.** Los iconos de Facebook, Instagram y TikTok están, pero
      **sin enlace**: se ven como si fueran botones y no llevan a ninguna parte.
- [ ] **Códigos de medición** (Google Analytics, píxel de Meta, Metricool). Vacíos: no se
      carga nada de terceros hasta que lleguen.
- [ ] **Archivo del logotipo horizontal** (emblema + nombre). El manual lo aprueba pero solo
      entregó el emblema. El nombre está compuesto con Manrope en `Logo.astro`.

## Decisiones abiertas

- **¿Cómo se entera el cliente si una publicación falla?** Hoy no se entera: GitHub avisa por
  correo solo al dueño de la cuenta (el proveedor). Opciones: que el agente compruebe el
  resultado y se lo cuente en la conversación, o un aviso por Telegram. Sin decidir.
- **Mapa.** Usa OpenStreetMap, un proyecto sin ánimo de lucro que desaconseja el tráfico de
  sitios comerciales; en pruebas ya rechazó parte de las imágenes. Si el sitio crece, pasar a
  un proveedor con plan gratuito (MapTiler, Protomaps) o a una imagen estática. Mientras
  tanto las direcciones siguen escritas y "Cómo llegar" funciona.

## Del manual de marca (para el diseñador)

- **El manual pide "texto blanco sobre azul"**, y sobre el azul oficial `#00AAFA` no se puede
  leer (2,58:1). Se resolvió con un azul más oscuro del mismo matiz. Si el diseñador quiere
  sostener la regla, el manual debería incluir ese azul de trabajo.
- **El logo maestro y la tabla de colores difieren un poco:** el SVG trae `#03863E`, `#FDD603`
  y `#8AC840`; la tabla del manual, `#00813F`, `#FFD400` y `#84CF3B`. Conviene unificarlos.

## Mejoras de datos (no bloquean)

- [ ] **Galerías de producto con fotos de otros productos.** Vienen así del sitio anterior:
      la segunda foto del Oscillococcinum es una caja de Aciclovir. Revisar producto por
      producto, o dejar solo la primera (campo `imagenes`).
- [ ] **Nombres de producto en mayúsculas.** El manual pide evitarlas. Pasarlos a minúsculas a
      ciegas estropea marcas y siglas: hacerlo al revisar el catálogo.
- [ ] **Subcategorías del 48% restante.** Se clasificó el 52% por palabras clave; el resto son
      genéricos que hay que revisar a mano.
