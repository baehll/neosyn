import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router"
import VueCookies from 'vue-cookies'
import axios from 'axios'
import FB_SDK from "./plugins"

axios.defaults.withCredentials = true;
const app = createApp(App);

app.use(VueCookies, {});
app.use(router);

/*
const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: address
});

app.provide('AXIOS_INSTANCE', axiosInstance);
*/

console.log(import.meta.env.VITE_FB_APP_ID)
console.log(import.meta.env.MODE)
if(import.meta.env.VITE_FB_APP_ID) {
    console.log("fb app id gesetzt")
    FB_SDK.initFacebookSdk(import.meta.env.VITE_FB_APP_ID)
}


app.mount('#app')
