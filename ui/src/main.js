import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router"
import VueCookies from 'vue-cookies'
import axios from 'axios'

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

app.mount('#app')
