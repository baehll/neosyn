import {createApp} from 'vue'
import {createPinia} from 'pinia';
import App from './App.vue'
import router from "./router"
import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faUserSecret} from '@fortawesome/free-solid-svg-icons'
import {createI18n} from 'vue-i18n';
import './style.css'
import timeDifference from './lib/TimeDifference.js';
const locale = document.querySelector('html').dataset.locale || 'en_US';

let modules = import.meta.glob('./languages/*.json', {eager: true});
const messages = modules[`./languages/${locale}.json`];
const app = createApp(App);
app.use(router)
app.use(createPinia())
app.use(timeDifference)
library.add(faUserSecret)
app.component('font-awesome-icon', FontAwesomeIcon);

const i18n = createI18n({
    locale,
    defaultLocale: 'en_US',
})

i18n.global.setLocaleMessage(locale, messages.default)
app.use(i18n)
app.mount('#app')
