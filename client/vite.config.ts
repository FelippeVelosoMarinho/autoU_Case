import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Garante que o Vite seja acessível publicamente
    port: 5173,       // Porta onde o Vite estará ouvindo
    allowedHosts: [
      'clientautoucase-production.up.railway.app',  // Adiciona o domínio da Railway
      'localhost',  // Adiciona localhost para testes locais
      '0.0.0.0',    // Adiciona a possibilidade de ser acessado por qualquer host
    ],
  },
})
