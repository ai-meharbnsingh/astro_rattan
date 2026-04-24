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
  build: {
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          // Vendor chunks
          if (id.includes('node_modules/react')) {
            return 'vendor-react';
          }
          if (id.includes('node_modules/@radix-ui')) {
            return 'vendor-ui';
          }
          if (id.includes('node_modules/recharts')) {
            return 'vendor-charts';
          }
          // Page-specific chunks (lazy load large pages)
          if (id.includes('LalKitabPage')) {
            return 'page-lalkitab';
          }
          if (id.includes('KundliGenerator')) {
            return 'page-kundli';
          }
          if (id.includes('NumerologyTarot')) {
            return 'page-numerology';
          }
          if (id.includes('VastuShastraPage')) {
            return 'page-vastu';
          }
          if (id.includes('HoroscopePage')) {
            return 'page-horoscope';
          }
          if (id.includes('AdminDashboard')) {
            return 'page-admin';
          }
        },
      },
    },
    chunkSizeWarningLimit: 600, // Increase limit to account for large pages
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:8010',
      '/ws': { target: 'ws://127.0.0.1:8010', ws: true },
    },
  },
});
