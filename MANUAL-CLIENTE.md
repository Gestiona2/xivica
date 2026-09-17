# Manual del dueño — Droguería Xivica

Cómo pedirle cambios a su asistente de la página, sin saber de tecnología.

## Cómo hablarle

Escríbale como me está escribiendo a mí: con sus palabras, sin tecnicismos.
Usted dice **qué quiere** ("cambie el teléfono", "ponga esta oferta") y yo me
encargo del resto. Si algo no se puede, se lo digo claro y le ofrezco la
alternativa.

## Lo que pasa cada vez que pide algo

1. **Hago el cambio** en una copia de trabajo. La página pública no se toca.
2. **Se lo muestro** en la vista previa (http://localhost:4321/ cuando trabajo,
   o el enlace de demostración). Le digo exactamente qué mirar.
3. **Usted aprueba** con un "se ve bien". El silencio no es aprobación.
4. **Lo publico.** Tarda de 2 a 4 minutos en verse. Si no lo ve, recargue con
   Ctrl+F5.
5. Si la publicación falla, **la página sigue mostrando la versión anterior**:
   nunca se rompe por un cambio.

## Lo que puedo hacer por usted (lo más común)

| Usted dice | Yo hago |
|---|---|
| "Cambie el precio de X" o me devuelve el Excel | Actualizo precios y ofertas, reviso que cuadren y le muestro |
| "Ponga esta promoción" + el texto | La pongo en la ventana que sale al abrir, en los destacados o donde me diga |
| "Quite esta promoción" | La apago (queda guardada por si vuelve) |
| "Cambie el teléfono / horario / dirección de una sede" | Lo cambio en todos los lados donde aparece |
| "Cambie el texto de tal parte" | Lo cambio; si es muy largo para celular, se lo advierto |
| "Agregue un producto" + datos y fotos | Lo creo con su precio, categoría y fotos |
| "Quite un producto" | Lo quito (queda guardado en el historial por si acaso) |
| "Marque este producto como agotado" | Sale el aviso de Agotado y no se puede agregar hasta que vuelva |
| "Cambie la foto de tal banner" | La pongo (apaisada, 800×500 pixeles) |
| "Cambie el WhatsApp / correo / NIT" | Lo cambio en toda la página |

## El Excel del catálogo

El archivo `Catalogo-Drogueria-Xivica.xlsx` trae los 407 productos:

- Edite **solo las celdas amarillas**. Las grises no se tocan.
- La columna **naranja** (¿requiere fórmula?) la llena **solo el regente**.
- Precios como número entero, sin puntos: `62900`. El % se calcula solo.
- En las casillas de SI/NO elija de la lista.
- **No agregue ni borre filas.** Para un producto nuevo o eliminado, avíseme.
- Me devuelve el archivo y **yo lo reviso producto por producto**: si algo quedó
  mal le digo qué producto, qué pasa y cómo se escribe bien. Nada se aplica
  hasta corregirlo.

## Lo que necesito que me dé usted (yo nunca lo invento)

- **Precios y ofertas.** Un precio mal puesto termina en discusión en el mostrador.
- **El texto de cada promoción** para la ventana emergente.
- **Indicaciones médicas** (para qué sirve algo, dosis): eso lo redacta el
  regente y yo lo copio tal cual.
- **Si un medicamento requiere fórmula**, lo confirma el regente. Yo nunca marco
  ni desmarco eso: marcar de menos un medicamento de control es un problema
  legal para la droguería.

## Todo se puede deshacer

| Usted dice | Yo hago |
|---|---|
| "No me gustó" (sin publicar) | Lo descarto, como si nada |
| "Devuélvalo como estaba" | Lo devuelvo y lo publico otra vez |
| "Vuelva a como estaba ayer" | Busco ese punto y lo devuelvo |
| "Borré algo sin querer" | Está guardado en el historial, lo recupero |

## Lo que NO hago yo (lo hace su proveedor Gestiona2, 301 366 5076)

Rediseñar la página, cambiar colores o letras por mi cuenta, poner pagos en
línea, conectar otros sistemas, cambiar el dominio o el correo, publicar sin su
aprobación, ni tocar contraseñas o configuraciones.

## Si algo raro pasa, deténgame y avíseme

- La vista previa no abre o muestra un error
- Dejan de llegar los mensajes del formulario
- Aparece un aviso de seguridad
- Le piden una contraseña para continuar

En esos casos no seguimos intentando: me dice qué ve y yo le digo con qué
palabras contárselo al proveedor.
