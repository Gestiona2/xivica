/**
 * Decide que productos salen destacados en la portada.
 *
 * Antes de esto el orden lo decidia el alfabeto, asi que la fila de
 * medicamentos abria con dos presentaciones de acetaminofen con codeina.
 *
 * El criterio, en este orden:
 *   1. Los marcados a mano con "destacado": true en productos.json.
 *   2. Los de mayor ahorro real en pesos.
 *   3. El resto, en un orden variado pero estable.
 *
 * `excluir` sirve para que un producto no aparezca dos veces en la misma
 * pantalla, en la fila de ofertas y otra vez en la de su categoria.
 *
 * Los productos que requieren formula medica quedan siempre fuera del
 * escaparate. Siguen en el catalogo y en el buscador para quien los busque.
 */

/**
 * Numero estable a partir de un texto.
 *
 * El relleno tiene que verse variado, pero NO puede cambiar entre
 * compilaciones: con Math.random la portada se reordenaria sola en cada
 * despliegue y generaria diferencias en Git sin que nadie tocara nada.
 */
function semilla(texto) {
  let valor = 0;
  for (let i = 0; i < texto.length; i++) {
    valor = (valor * 31 + texto.charCodeAt(i)) % 2147483647;
  }
  return valor;
}

const ahorro = (producto) =>
  producto.precio_antes && producto.precio_antes > producto.precio
    ? producto.precio_antes - producto.precio
    : 0;

export function elegirDestacados(productos, cantidad, opciones = {}) {
  const { excluirRx = true, excluir = new Set() } = opciones;

  const elegibles = productos.filter(
    (p) => !excluir.has(p.slug) && (!excluirRx || p.rx !== true)
  );

  const marcados = elegibles.filter((p) => p.destacado === true);
  const resto = elegibles.filter((p) => p.destacado !== true);

  const conAhorro = resto
    .filter((p) => ahorro(p) > 0)
    .sort((a, b) => ahorro(b) - ahorro(a));

  const sinAhorro = resto
    .filter((p) => ahorro(p) === 0)
    .sort((a, b) => semilla(a.slug) - semilla(b.slug));

  const vistos = new Set();
  const salida = [];
  for (const producto of [...marcados, ...conAhorro, ...sinAhorro]) {
    if (salida.length >= cantidad) break;
    if (vistos.has(producto.slug)) continue;
    vistos.add(producto.slug);
    salida.push(producto);
  }
  return salida;
}
