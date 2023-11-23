import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig( async ({command, mode}) => {
    let configObj = {
        plugins: [vue()]
    };
    if (mode === 'development') {
        const sslPlugin = await import('@vitejs/plugin-basic-ssl')
        configObj.plugins.push(sslPlugin.default())
    }

    return configObj;
})
