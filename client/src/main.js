import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router"
import VueCookies from 'vue-cookies'
import axios from 'axios'
import { createPinia } from 'pinia'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'

import VueSidebarMenu from "vue-sidebar-menu"
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

function startApp() {
    axios.defaults.withCredentials = true;
    const app = createApp(App);

    setupIconLibrary(app);
    setupUseCalls(app);

    app.mount('#app')
}


function setupIconLibrary(app) {
    library.add(faUserSecret)
    app.component('font-awesome-icon', FontAwesomeIcon);

}

function setupUseCalls(app) {
    let axiosConfig = {
        withCredentials: true,
        baseURL: import.meta.env.VITE_BASE_URL
    };

    if(localStorage.getItem("token") != null) {
        axiosConfig["headers"] = {"Authorization" : "Bearer " + localStorage.getItem("token")}
    }
    const axiosInstance = axios.create(axiosConfig);
    const pinia = createPinia();
    app.use(pinia);

    app.provide('AXIOS_INSTANCE', axiosInstance);
    app.provide("VITE_FB_APP_ID", import.meta.env.VITE_FB_APP_ID)
    app.use(VueCookies, {});
    app.use(router);
    app.use(VueSidebarMenu) 
}

startApp()