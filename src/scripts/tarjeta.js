/**
 * La tarjeta de producto en JavaScript, para las listas que se pintan en el
 * navegador (catalogo filtrado, favoritos).
 *
 * Tiene que verse igual que components/TarjetaProducto.astro. Si se cambia
 * una, hay que cambiar la otra: esta anotado en conocimiento_generado/LIMITES.md.
 */
import { pesos } from "./formato.js";

const escapar = (texto) =>
  String(texto).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );

export function tarjetaHTML(producto, base) {
  const ahorro = producto.precio_antes ? producto.precio_antes - producto.precio : null;
  return `
    <article class="tarjeta" data-slug="${producto.slug}">
      ${producto.descuento ? `<span class="tarjeta-descuento">-${producto.descuento}%</span>` : ""}
      <button type="button" class="tarjeta-favorito" data-favorito="${producto.slug}"
              aria-label="Guardar ${escapar(producto.titulo)} en favoritos" aria-pressed="false">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M12 20.3s-7.2-4.6-7.2-9.6a4 4 0 0 1 7.2-2.4 4 4 0 0 1 7.2 2.4c0 5-7.2 9.6-7.2 9.6Z"/>
        </svg>
      </button>
      <a href="${base}producto/${producto.slug}" class="tarjeta-foto">
        <img src="${base}img/${producto.imagenes[0]}" alt="${escapar(producto.titulo)}"
             width="220" height="220" loading="lazy" decoding="async">
      </a>
      <div class="tarjeta-cuerpo">
        ${producto.marca ? `<span class="tarjeta-marca">${escapar(producto.marca)}</span>` : ""}
        <h3 class="tarjeta-titulo"><a href="${base}producto/${producto.slug}">${escapar(producto.titulo)}</a></h3>
        ${producto.presentacion ? `<p class="tarjeta-presentacion">${escapar(producto.presentacion)}</p>` : ""}
        <div class="tarjeta-precio">
          ${producto.precio_antes ? `<s class="tarjeta-antes">${pesos(producto.precio_antes)}</s>` : ""}
          <strong>${pesos(producto.precio)}</strong>
          ${ahorro ? `<span class="tarjeta-ahorro">Ahorras ${pesos(ahorro)}</span>` : ""}
        </div>
        <button type="button" class="boton boton-azul tarjeta-agregar"
                data-agregar="${producto.slug}" data-titulo="${escapar(producto.titulo)}"
                data-precio="${producto.precio}" data-imagen="${producto.imagenes[0]}">Agregar</button>
      </div>
    </article>`;
}

