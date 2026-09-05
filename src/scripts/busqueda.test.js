import { test } from "node:test";
import assert from "node:assert/strict";
import { construirIndice, buscar } from "./busqueda.js";

const CATALOGO = [
  { slug: "aceta", titulo: "ACETAMINOFÉN 500 MG X 20 TAB", marca: null,
    categoria: "medicamentos", subcategoria: "analgesicos", precio: 5000 },
  { slug: "nivea", titulo: "CREMA NIVEA BODY MILK ALMENDRAS 125 ML", marca: "Nivea",
    categoria: "cuidado-personal", subcategoria: "cuidado-piel", precio: 8200 },
  { slug: "dolex", titulo: "DOLEX FORTE 20 TABLETAS", marca: "Dolex",
    categoria: "medicamentos", subcategoria: "analgesicos", precio: 12000 },
];
const indice = construirIndice(CATALOGO);

test("encuentra sin tildes lo que está escrito con tildes", () => {
  assert.equal(buscar(indice, "acetaminofen")[0].slug, "aceta");
});

test("da igual mayúsculas o minúsculas", () => {
  assert.equal(buscar(indice, "NIVEA")[0].slug, "nivea");
  assert.equal(buscar(indice, "nivea")[0].slug, "nivea");
});

test("aguanta un error de tipeo", () => {
  // sobra una letra
  assert.equal(buscar(indice, "acetaminofeno")[0].slug, "aceta");
  // falta una letra
  assert.equal(buscar(indice, "acetaminfen")[0].slug, "aceta");
  // letra cambiada
  assert.equal(buscar(indice, "nivae")[0].slug, "nivea");
});

test("encuentra por varias palabras sueltas y en cualquier orden", () => {
  assert.equal(buscar(indice, "crema almendras")[0].slug, "nivea");
  assert.equal(buscar(indice, "almendras crema")[0].slug, "nivea");
});

test("encuentra por marca y por lo que sirve", () => {
  assert.equal(buscar(indice, "dolex")[0].slug, "dolex");
  assert.equal(buscar(indice, "analgesicos").length, 2);
});

test("lo que empieza igual que lo buscado va primero", () => {
  const salida = buscar(indice, "dol");
  assert.equal(salida[0].slug, "dolex");
});

test("lo que no existe no devuelve nada", () => {
  assert.deepEqual(buscar(indice, "zzzzqqq"), []);
});

test("una búsqueda vacía no devuelve el catálogo entero", () => {
  assert.deepEqual(buscar(indice, ""), []);
  assert.deepEqual(buscar(indice, "   "), []);
});

test("se puede limitar cuántos resultados devuelve", () => {
  assert.equal(buscar(indice, "medicamentos", { limite: 1 }).length, 1);
});

test("las palabras sin contenido no impiden encontrar", () => {
  // "para" y "la" no aparecen en ningun nombre de producto
  assert.equal(buscar(indice, "crema para la piel")[0].slug, "nivea");
  assert.equal(buscar(indice, "crema de almendras")[0].slug, "nivea");
});

test("una busqueda solo de palabras vacias no devuelve nada", () => {
  assert.deepEqual(buscar(indice, "de la para"), []);
});

test("los sinonimos encuentran productos que no se llaman asi", () => {
  const catalogo = [
    { slug: "winny", titulo: "WINNY ULT/SEC ET.5 PAQ X 30", marca: null,
      categoria: "bebe-maternidad", subcategoria: "bebe", precio: 30000 },
  ];
  const idx = construirIndice(catalogo, { panales: ["winny"] });
  assert.equal(buscar(idx, "panales")[0].slug, "winny");
  assert.equal(buscar(idx, "pañales")[0].slug, "winny");
});
