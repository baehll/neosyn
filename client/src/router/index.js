import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Registration from '../views/Registration.vue';
import InboxView from '../views/InboxView.vue';

const routes = [
    {
        path: "/",
        name: "Index",
        component: Home,
    },
    {
        path: "/inbox",
        name: "Inbox",
        component: InboxView
    },
    {
        path: "/register",
        name: "Registration",
        component: Registration
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: Login
    },
]
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
