import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5198,
    proxy: {
      '/api': 'http://localhost:8028',
      '/ws': { target: 'ws://localhost:8028', ws: true },
    },
  },
});
