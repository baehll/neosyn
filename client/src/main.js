import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router"
import VueCookies from 'vue-cookies'
import axios from 'axios'
import { createPinia } from 'pinia'
import { useFBStore } from './store/fb'

axios.defaults.withCredentials = true;
const app = createApp(App);
const pinia = createPinia();

app.use(VueCookies, {});
app.use(router);
app.use(pinia);


const store = useFBStore();

/*
const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: address
});

app.provide('AXIOS_INSTANCE', axiosInstance);

if(import.meta.env.VITE_FB_APP_ID) {
    FB_SDK.initFacebookSdk(import.meta.env.VITE_FB_APP_ID).then(startApp());
} else {
    app.mount('#app')
}
*/


function startApp() {
    fbEvents();
    app.mount('#app')
}

function fbEvents() {
    window.addEventListener("fb-ready", () => {
        // Pinia Store mit den Daten befüllen
        FB.getLoginStatus((fbRes) => {
            if(fbRes && fbRes.status !== 'connected') {
                FB.login((res) => {
                    if(res.authResponse) {
                        console.log("logged in")
                    }
                }, {scope: 'instagram_basic,pages_show_list'})
            } else {
                store.populateData();
            }
            console.log("fb sdk ready");
        })
    })
}

startApp()