import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Registration from '../views/Registration.vue';

const routes = [
    {
        path: "/",
        name: "Home",
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
    {
        path: "/login",
        name: "Login",
        component: Login
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

// Hiermit wird sichergestellt, dass nur authentifizierte Nutzer auf die wichtigen Seiten zugreifen können
/*
router.beforeEach((to, from, next) => {

    const authStore = useAuthStore();
    if(to.matched.some(r =>  r.meta.requiresAuth)) {
        if(!authStore.isAuthenticated()) {
            next("/");
        } else {
            next()
        }
    } else if (to.path === "/" && authStore.isAuthenticated()){
        next("/dashboard")
    } else {
        next()
    }
})
*/
export default router