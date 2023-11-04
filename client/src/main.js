import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router"
import VueCookies from 'vue-cookies'
import axios from 'axios'
import { createPinia } from 'pinia'
import { useFBStore } from './store/fb'

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
    
    const stores = initCustomStores();
    fbEvents(stores);

    app.mount('#app')
}

function fbEvents(stores) {
    window.addEventListener("fb-ready", () => {
        // Pinia Store mit den Daten befüllen
        FB.getLoginStatus((fbRes) => {
            if(fbRes && fbRes.status !== 'connected') {
                FB.login((res) => {
                    if(res.authResponse) {
                        console.log("logged in")
                    }
                }, {scope: 'pages_show_list,business_management,instagram_basic,instagram_manage_comments,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_engagement,public_profile'})
            }
            stores.fbStore.populateData();
            stores.fbStore.sendAuthTokens();
        })
    })
}

function setupIconLibrary(app) {
    library.add(faUserSecret)
    app.component('font-awesome-icon', FontAwesomeIcon);

}

function setupUseCalls(app) {
    
    const axiosInstance = axios.create({
        withCredentials: true,
        baseURL: "http://localhost:5000"
    });
    const pinia = createPinia();

    app.provide('AXIOS_INSTANCE', axiosInstance);
    app.use(VueCookies, {});
    app.use(router);
    app.use(pinia);
    app.use(VueSidebarMenu) 
}

function initCustomStores() {
    return {
        fbStore: useFBStore()
    }
}

startApp()