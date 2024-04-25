import {createApp} from 'vue'
import {createPinia} from 'pinia';
import router from "./router/site"
import {library} from '@fortawesome/fontawesome-svg-core'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faUserSecret} from '@fortawesome/free-solid-svg-icons'
import {createI18n} from 'vue-i18n';
import './style.css'
import Site from './Site.vue';
const locale = document.querySelector('html').dataset.locale || 'en_US';

let modules = import.meta.glob('./languages/*.json', {eager: true});
const messages = modules[`./languages/${locale}.json`];
const app = createApp(Site);
app.use(router)
app.use(createPinia())
library.add(faUserSecret)
app.component('font-awesome-icon', FontAwesomeIcon);

const i18n = createI18n({
    locale,
    defaultLocale: 'en_US',
})

i18n.global.setLocaleMessage(locale, messages.default)
app.use(i18n)
app.mount(document.getElementById('app') ? '#app' : '#splash')
