import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Isso faz o Vite ouvir em todas as interfaces de rede
    port: 5173,       // Se quiser especificar a porta, por exemplo 5173
  },
})
