/**
 * Mapas de las sedes.
 *
 * Leaflet no se carga con la pagina: se descarga cuando el mapa esta a punto
 * de entrar en pantalla. Son unos 150 KB entre codigo y estilos, y la mayoria
 * de visitantes viene a comprar, no a mirar donde quedan las sedes.
 *
 * Las imagenes del mapa las sirve OpenStreetMap, asi que esto es lo unico del
 * sitio que depende de un servidor ajeno. Si no carga, debajo del mapa quedan
 * las direcciones escritas y los enlaces a Google Maps, que siempre funcionan.
 */
const LEAFLET_CSS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
const LEAFLET_JS = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";

let cargando = null;

function cargarLeaflet() {
  if (window.L) return Promise.resolve(window.L);
  if (cargando) return cargando;

  cargando = new Promise((resolver, rechazar) => {
    const estilos = document.createElement("link");
    estilos.rel = "stylesheet";
    estilos.href = LEAFLET_CSS;
    document.head.appendChild(estilos);

    const script = document.createElement("script");
    script.src = LEAFLET_JS;
    script.onload = () => resolver(window.L);
    script.onerror = () => rechazar(new Error("No se pudo cargar el mapa"));
    document.head.appendChild(script);
  });
  return cargando;
}

export function montarMapaSedes() {
  const caja = document.getElementById("mapaSedes");
  if (!caja) return;

  const sedes = JSON.parse(caja.dataset.sedes || "[]");
  if (sedes.length === 0) return;

  const dibujar = async () => {
    let L;
    try {
      L = await cargarLeaflet();
    } catch {
      caja.innerHTML =
        '<p class="mapa-falla">No se pudo cargar el mapa. Las direcciones están escritas arriba.</p>';
      return;
    }

    const mapa = L.map(caja, { scrollWheelZoom: false }).setView(
      [sedes[0].lat, sedes[0].lng],
      14
    );
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap",
      maxZoom: 19,
    }).addTo(mapa);

    const marcas = {};
    sedes.forEach((sede) => {
      marcas[sede.id] = L.marker([sede.lat, sede.lng])
        .addTo(mapa)
        .bindPopup(
          `<strong>${sede.nombre}</strong><br>${sede.direccion}<br>` +
            `<a href="https://www.google.com/maps/search/?api=1&query=${sede.lat},${sede.lng}" ` +
            `target="_blank" rel="noopener">Cómo llegar</a>`
        );
    });

    if (sedes.length > 1) {
      mapa.fitBounds(sedes.map((s) => [s.lat, s.lng]), { padding: [50, 50] });
    }

    document.querySelectorAll("[data-ver-sede]").forEach((boton) => {
      boton.addEventListener("click", () => {
        const sede = sedes.find((s) => s.id === boton.dataset.verSede);
        if (!sede) return;
        mapa.setView([sede.lat, sede.lng], 16);
        marcas[sede.id].openPopup();
        caja.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    });
  };

  if (!("IntersectionObserver" in window)) return dibujar();

  const observador = new IntersectionObserver(
    (entradas) => {
      if (entradas[0].isIntersecting) {
        observador.disconnect();
        dibujar();
      }
    },
    { rootMargin: "300px" }
  );
  observador.observe(caja);
}
