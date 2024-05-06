import {createRouter, createWebHashHistory, createWebHistory} from 'vue-router';
import Login from '../views/Login.vue';
import InboxView from '../views/InboxView.vue';
import Dashboard from '../views/Dashboard.vue';

const routes = [
    {
        path: "/",
        name: "Index",
        component: Dashboard,
    },
    {
        path: "/inbox",
        name: "Inbox",
        component: InboxView
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: Login
    },
]
const router = createRouter({
    history:createWebHashHistory(import.meta.env.BASE_URL + 'app.html'),
    routes,

})

export default router
