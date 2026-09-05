import { test } from "node:test";
import assert from "node:assert/strict";
import { elegirDestacados } from "./destacados.js";

const p = (slug, extra = {}) => ({
  slug, titulo: slug.toUpperCase(), precio: 10000, precio_antes: null,
  descuento: null, categoria: "medicamentos", rx: null, destacado: false, ...extra,
});

test("los marcados a mano van primero, en el orden en que estén", () => {
  const lista = [p("a"), p("b", { destacado: true }), p("c", { destacado: true })];
  const salida = elegirDestacados(lista, 3);
  assert.deepEqual(salida.slice(0, 2).map((x) => x.slug), ["b", "c"]);
});

test("cuando faltan, se completa con los de mayor ahorro en pesos", () => {
  const lista = [
    p("poco", { precio: 9000, precio_antes: 10000 }),   // ahorra 1.000
    p("mucho", { precio: 50000, precio_antes: 80000 }), // ahorra 30.000
    p("nada"),
  ];
  const salida = elegirDestacados(lista, 2);
  assert.deepEqual(salida.map((x) => x.slug), ["mucho", "poco"]);
});

test("si aún faltan, se rellena con el resto", () => {
  const lista = [p("a"), p("b"), p("c")];
  assert.equal(elegirDestacados(lista, 3).length, 3);
});

test("los que requieren fórmula médica nunca salen destacados", () => {
  const lista = [
    p("controlado", { rx: true, precio: 1000, precio_antes: 90000 }), // el que más ahorra
    p("normal"),
  ];
  const salida = elegirDestacados(lista, 5);
  assert.deepEqual(salida.map((x) => x.slug), ["normal"]);
});

test("un producto marcado a mano tampoco entra si requiere fórmula", () => {
  const salida = elegirDestacados([p("x", { destacado: true, rx: true }), p("y")], 2);
  assert.deepEqual(salida.map((x) => x.slug), ["y"]);
});

test("el relleno al azar es el mismo en cada compilación", () => {
  const lista = "abcdefghij".split("").map((s) => p(s));
  const una = elegirDestacados(lista, 4).map((x) => x.slug);
  const otra = elegirDestacados(lista, 4).map((x) => x.slug);
  assert.deepEqual(una, otra, "la portada cambiaría en cada build");
});

test("no devuelve más de los pedidos ni repite productos", () => {
  const lista = "abcdefghij".split("").map((s) => p(s, { destacado: s === "a" }));
  const salida = elegirDestacados(lista, 5);
  assert.equal(salida.length, 5);
  assert.equal(new Set(salida.map((x) => x.slug)).size, 5);
});

test("pedir más de los que hay devuelve todos los disponibles", () => {
  assert.equal(elegirDestacados([p("a"), p("b")], 10).length, 2);
});

test("se pueden excluir productos ya mostrados en otra fila", () => {
  const lista = [p("a"), p("b"), p("c")];
  const salida = elegirDestacados(lista, 2, { excluir: new Set(["a"]) });
  assert.deepEqual(salida.map((x) => x.slug).sort(), ["b", "c"]);
});
