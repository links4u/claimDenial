import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        host: '0.0.0.0',
        port: 2400,
        proxy: {
            '/api': {
                target: 'http://localhost:1500',
                changeOrigin: true,
            }
        }
    }
})
