import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

// El sitio se publica primero como demo en GitHub Pages bajo /xivica/ y luego
// en el dominio propio del cliente en la raiz. Por eso `base` es una variable
// de entorno: mudarlo es cambiar un valor, no reescribir rutas.
//   demo:       PUBLIC_BASE=/xivica/ PUBLIC_SITE=https://gestiona2.github.io
//   produccion: (sin variables, o las del dominio definitivo)
export default defineConfig({
  site: process.env.PUBLIC_SITE || "https://gestiona2.github.io",
  base: process.env.PUBLIC_BASE || "/",
  vite: {
    plugins: [tailwindcss()],
  },
});
