import {resolve} from 'path';
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig( async ({command, mode}) => {
    let configObj = {
        plugins: [vue()],
        rollupOptions: {
           input: {
               comingsoon: resolve(__dirname, `./index.html`),
               registration: resolve(__dirname, './registration.html'),
               app: resolve(__dirname, './app.html'),
           }
        }
    };
    if (mode === 'development') {
        const sslPlugin = await import('@vitejs/plugin-basic-ssl')
        configObj.plugins.push(sslPlugin.default())
    }

    return configObj;
})
