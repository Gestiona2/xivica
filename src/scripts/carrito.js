/**
 * Panel del carrito: lo que se ve y se toca.
 *
 * La logica del pedido (sumas, cantidades, mensaje) vive en pedido.js y se
 * prueba aparte. Aqui solo esta la interfaz.
 *
 * El pedido se guarda en el navegador para que no se pierda al cambiar de
 * pagina ni al volver mas tarde. Todos los accesos van envueltos en try/catch
 * porque en ventana privada el navegador puede lanzar excepcion al leerlos.
 */
import { crearPedido, armarMensaje, enlaceWhatsApp } from "./pedido.js";
import { pesos } from "./formato.js";

const CLAVE = "xivica-pedido";

const guardar = (lineas) => {
  try {
    localStorage.setItem(CLAVE, JSON.stringify(lineas));
  } catch {
    /* ventana privada o almacenamiento lleno: el carrito sigue funcionando
       durante la visita, solo no sobrevive al cierre */
  }
};

const recuperar = () => {
  try {
    return JSON.parse(localStorage.getItem(CLAVE) || "[]");
  } catch {
    return [];
  }
};

const escapar = (texto) =>
  String(texto).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );

export function montarCarrito() {
  const panel = document.getElementById("carrito");
  const cuerpo = document.getElementById("carritoCuerpo");
  if (!panel || !cuerpo) return;

  const base = document.documentElement.dataset.base || "/";
  const whatsapp = panel.dataset.whatsapp || "";
  const envioGratisDesde = Number(panel.dataset.envio || 60000);

  const fondo = document.getElementById("carritoFondo");
  const barra = document.getElementById("barraPago");
  const globoCarrito = document.querySelector('[data-contador="carrito"] .accion-globo');

  const pedido = crearPedido({
    envioGratisDesde,
    alCambiar: (p) => {
      guardar(p.exportar());
      pintarContadores(p);
      if (!panel.hidden) pintarPanel(p);
    },
  });

  /* ---------- contadores de la cabecera y barra inferior ---------- */
  function pintarContadores(p) {
    const unidades = p.unidades();

    if (globoCarrito) {
      globoCarrito.textContent = unidades;
      globoCarrito.hidden = unidades === 0;
    }

    barra.hidden = unidades === 0;
    if (unidades > 0) {
      document.getElementById("barraPagoTotal").textContent = pesos(p.total());
      document.getElementById("barraPagoItems").textContent =
        unidades === 1 ? "1 producto" : `${unidades} productos`;
    }
  }

  /* ---------- panel ---------- */
  function pintarPanel(p) {
    const lineas = p.lineas();

    if (lineas.length === 0) {
      cuerpo.innerHTML = `
        <div class="carrito-vacio">
          <p>Tu pedido está vacío.</p>
          <a class="boton boton-azul" href="${base}catalogo">Ver el catálogo</a>
        </div>`;
      return;
    }

    const falta = p.faltaParaEnvioGratis();

    cuerpo.innerHTML = `
      <div class="carrito-columnas">
        <div class="carrito-lista">
          ${lineas
            .map(
              (linea) => `
            <article class="carrito-linea" data-slug="${linea.slug}">
              <img src="${base}img/${linea.imagen}" alt="" width="64" height="64" loading="lazy">
              <div class="carrito-linea-datos">
                <a href="${base}producto/${linea.slug}">${escapar(linea.titulo)}</a>
                <span class="carrito-linea-unitario">${pesos(linea.precio)} c/u</span>
              </div>
              <div class="carrito-cantidad">
                <button type="button" data-menos="${linea.slug}" aria-label="Quitar una unidad">−</button>
                <span aria-live="polite">${linea.cantidad}</span>
                <button type="button" data-mas="${linea.slug}" aria-label="Agregar una unidad">+</button>
              </div>
              <strong class="carrito-linea-total">${pesos(linea.precio * linea.cantidad)}</strong>
              <button type="button" class="carrito-quitar" data-quitar="${linea.slug}"
                      aria-label="Quitar ${escapar(linea.titulo)} del pedido">×</button>
            </article>`
            )
            .join("")}
        </div>

        <form class="carrito-datos" id="formPedido" novalidate>
          <h3>Datos de entrega</h3>

          <label>Nombre y apellido
            <input name="nombre" required autocomplete="name" placeholder="Ana Gómez">
          </label>
          <label>Teléfono
            <input name="telefono" required inputmode="tel" autocomplete="tel" placeholder="300 123 4567">
          </label>
          <label>Dirección
            <input name="direccion" required autocomplete="street-address" placeholder="Cra 49B #171a-92 apto 302">
          </label>
          <label>Barrio <span class="opcional">(opcional)</span>
            <input name="barrio" autocomplete="address-level3" placeholder="Villa del Prado">
          </label>
          <label>Forma de pago
            <select name="pago">
              <option>Efectivo</option>
              <option>Transferencia (Nequi / Daviplata)</option>
              <option>Datáfono en la entrega</option>
            </select>
          </label>
          <label>Nota para el domiciliario <span class="opcional">(opcional)</span>
            <textarea name="nota" rows="2" placeholder="El timbre no sirve, llamar al llegar"></textarea>
          </label>

          <div class="carrito-total">
            ${
              falta > 0
                ? `<p class="carrito-envio">Te faltan <strong>${pesos(falta)}</strong> para el domicilio gratis</p>`
                : `<p class="carrito-envio carrito-envio-listo">Domicilio gratis</p>`
            }
            <div class="carrito-total-linea">
              <span>Total</span>
              <strong>${pesos(p.total())}</strong>
            </div>
            <button type="submit" class="boton boton-lima carrito-enviar">
              Enviar pedido por WhatsApp
            </button>
            <p class="carrito-nota">
              Al enviar se abre WhatsApp con tu pedido escrito. La droguería confirma
              disponibilidad y tiempo de entrega antes de despachar.
            </p>
          </div>
        </form>
      </div>`;

    cuerpo.querySelector("#formPedido").addEventListener("submit", enviarPedido);
  }

  /* ---------- enviar ---------- */
  function enviarPedido(evento) {
    evento.preventDefault();
    const formulario = evento.target;
    const datos = Object.fromEntries(new FormData(formulario));

    const faltantes = ["nombre", "telefono", "direccion"].filter(
      (campo) => !String(datos[campo] || "").trim()
    );
    if (faltantes.length > 0) {
      const campo = formulario.elements[faltantes[0]];
      campo.focus();
      campo.classList.add("campo-falta");
      avisar("Falta " + { nombre: "tu nombre", telefono: "tu teléfono", direccion: "la dirección" }[faltantes[0]]);
      return;
    }

    const mensaje = armarMensaje(pedido, datos);
    window.open(enlaceWhatsApp(whatsapp, mensaje), "_blank", "noopener");

    guardarEnHistorial(pedido);
    avisar("Pedido enviado. Revisa WhatsApp.");
  }

  function guardarEnHistorial(p) {
    try {
      const historial = JSON.parse(localStorage.getItem("xivica-historial") || "[]");
      historial.unshift({ fecha: new Date().toISOString(), lineas: p.exportar() });
      localStorage.setItem("xivica-historial", JSON.stringify(historial.slice(0, 20)));
    } catch {
      /* sin historial, el pedido igual se envio */
    }
  }

  /* ---------- abrir y cerrar ---------- */
  let ultimoFoco = null;

  const abrir = () => {
    ultimoFoco = document.activeElement;
    panel.hidden = false;
    fondo.hidden = false;
    requestAnimationFrame(() => panel.classList.add("abierto"));
    panel.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    pintarPanel(pedido);
    panel.querySelector("#cerrarCarrito")?.focus();
  };

  const cerrar = () => {
    panel.classList.remove("abierto");
    panel.setAttribute("aria-hidden", "true");
    fondo.hidden = true;
    document.body.style.overflow = "";
    setTimeout(() => (panel.hidden = true), 280);
    ultimoFoco?.focus();
  };

  document.getElementById("abrirCarrito")?.addEventListener("click", abrir);
  document.getElementById("barraPagoBoton")?.addEventListener("click", abrir);
  document.getElementById("cerrarCarrito")?.addEventListener("click", cerrar);
  fondo?.addEventListener("click", cerrar);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !panel.hidden) cerrar();
  });

  /* ---------- botones de agregar, en toda la pagina ---------- */
  document.addEventListener("click", (evento) => {
    const agregar = evento.target.closest("[data-agregar]");
    if (agregar) {
      pedido.agregar(
        {
          slug: agregar.dataset.agregar,
          titulo: agregar.dataset.titulo,
          precio: Number(agregar.dataset.precio),
          imagen: agregar.dataset.imagen,
        },
        1
      );
      avisar(`${agregar.dataset.titulo} agregado`);
      return;
    }

    const mas = evento.target.closest("[data-mas]");
    if (mas) {
      const linea = pedido.lineas().find((l) => l.slug === mas.dataset.mas);
      pedido.cambiarCantidad(mas.dataset.mas, linea.cantidad + 1);
      return;
    }

    const menos = evento.target.closest("[data-menos]");
    if (menos) {
      const linea = pedido.lineas().find((l) => l.slug === menos.dataset.menos);
      pedido.cambiarCantidad(menos.dataset.menos, linea.cantidad - 1);
      return;
    }

    const quitar = evento.target.closest("[data-quitar]:not([data-valor])");
    if (quitar && quitar.classList.contains("carrito-quitar")) {
      pedido.quitar(quitar.dataset.quitar);
    }
  });

  /* ---------- aviso flotante ---------- */
  let temporizadorAviso = null;
  function avisar(texto) {
    let aviso = document.getElementById("aviso");
    if (!aviso) {
      aviso = document.createElement("div");
      aviso.id = "aviso";
      aviso.className = "aviso";
      aviso.setAttribute("role", "status");
      document.body.appendChild(aviso);
    }
    aviso.textContent = texto;
    aviso.classList.add("visible");
    clearTimeout(temporizadorAviso);
    temporizadorAviso = setTimeout(() => aviso.classList.remove("visible"), 2600);
  }

  // "Repetir pedido" desde la pagina de volver a comprar
  document.addEventListener("pedido:agregar", (evento) => {
    const { producto, cantidad } = evento.detail;
    pedido.agregar(producto, cantidad || 1);
    avisar("Productos agregados a tu pedido");
  });

  pedido.importar(recuperar());
  pintarContadores(pedido);
}
