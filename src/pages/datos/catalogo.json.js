/**
 * Catalogo ligero que descarga el buscador.
 *
 * Se genera en la compilacion a partir de productos.json, quitando lo que el
 * buscador no necesita (descripcion, galeria completa, trazabilidad). Asi no
 * hay dos archivos que mantener sincronizados: este sale del otro.
 */
import productos from "../../datos/productos.json";

export function GET() {
  const ligero = productos.map((p) => ({
    slug: p.slug,
    titulo: p.titulo,
    precio: p.precio,
    precio_antes: p.precio_antes,
    descuento: p.descuento,
    categoria: p.categoria,
    subcategoria: p.subcategoria,
    marca: p.marca,
    presentacion: p.presentacion,
    rx: p.rx,
    imagenes: p.imagenes.slice(0, 1),
  }));

  return new Response(JSON.stringify(ligero), {
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
}
