import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Registration from '../views/Registration.vue';
import ComingSoon from '../views/ComingSoon.vue';
import Imprint from '../views/Imprint.vue';
import PrivacyPolicy from '../views/PrivacyPolicy.vue';

const routes = [
    {
        path: "/",
        name: "Home",
        component: ComingSoon
    },
    {
        path: "/imprint",
        name: "Imprint",
        component: Imprint
    },
    {
        path: "/privacy-policy",
        name: "Privacy Policy",
        component: PrivacyPolicy
    },
    {
        path: "/index",
        name: "Index",
        component: Home
    },
    {
        path: "/login",
        name: "Login",
        component: Login
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
