// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    // Evita duplicados de React cuando alguna lib trae su propia copia
    dedupe: ["react", "react-dom"],
  },
  define: {
    // Algunas libs (MUI/RA ecosistema) esperan estos símbolos
    "process.env": {},
    global: "window",
  },
  server: {
    host: true,       // accesible en LAN
    port: 5173,
    open: true,       // abre el navegador al levantar
  },
  preview: {
    host: true,
    port: 4173,
    open: true,
  },
  optimizeDeps: {
    include: ["react", "react-dom", "react-dom/client"],
  },
  build: {
    target: "es2020",
    sourcemap: true,
    outDir: "dist",
  },
  css: {
    // Usa tu configuración de PostCSS (Tailwind)
    postcss: "./postcss.config.js",
  },
});
