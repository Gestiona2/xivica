// Se corre con: node --test src/scripts/
import { test } from "node:test";
import assert from "node:assert/strict";
import { pesos, sinTildes, porcentajeAhorro } from "./formato.js";

test("los pesos se muestran como en Colombia, con punto de miles", () => {
  assert.equal(pesos(62900), "$62.900");
  assert.equal(pesos(8200), "$8.200");
  assert.equal(pesos(1234567), "$1.234.567");
  assert.equal(pesos(0), "$0");
});

test("un precio ausente no imprime 'NaN' en la tienda", () => {
  assert.equal(pesos(null), "");
  assert.equal(pesos(undefined), "");
});

test("sinTildes permite buscar 'acetaminofen' y encontrar 'ACETAMINOFÉN'", () => {
  assert.equal(sinTildes("ACETAMINOFÉN"), "acetaminofen");
  assert.equal(sinTildes("Bebé y Maternidad"), "bebe y maternidad");
  assert.equal(sinTildes("NIÑOS"), "ninos");
});

test("el ahorro se calcula sobre el precio anterior", () => {
  assert.equal(porcentajeAhorro(84915, 62900), 26);
  assert.equal(porcentajeAhorro(null, 62900), null);
  // un precio mayor que el anterior no es una oferta
  assert.equal(porcentajeAhorro(1000, 2000), null);
});
