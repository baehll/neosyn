import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue';

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home
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