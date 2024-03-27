import { createRouter, createWebHistory } from 'vue-router'
import ComingSoon from '../views/ComingSoon.vue';
import Imprint from '../views/Imprint.vue';
import PrivacyPolicy from '../views/PrivacyPolicy.vue';
import Registration from '../views/Registration.vue';

const routes = [
    {
        path: "/",
        name: "Home",
        component: ComingSoon
    },
    {
        path: "/register",
        name: "Registration",
        component: Registration
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
]
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
