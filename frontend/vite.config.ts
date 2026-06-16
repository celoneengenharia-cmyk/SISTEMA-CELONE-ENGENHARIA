import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// O frontend roda em :5173 e fala com o backend em :8000.
// O proxy evita lidar com CORS no dia a dia de desenvolvimento.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (p) => p.replace(/^\/api/, ""),
      },
    },
  },
});
