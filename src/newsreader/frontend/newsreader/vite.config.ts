import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// {require} = path('resolve');
// https://vitejs.dev/config/
export default defineConfig({
  root: '',
  base: '/static/',
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  plugins: [vue()]
})
