import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from "../views/landingpage/LandingPage.vue"
import Login from "../views/Login.vue"
import Dashboard from "../views/landingpage/children/Dashboard.vue"
import InteractionsPage from "../views/interactions/InteractionsPage.vue"
import { useAuthStore } from '../store/auth'
import { parseJwt } from "../utils"

const routes = [
    {
        path: "/",
        name: "Login",
        component: Login
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: Dashboard,
        meta: { requiresAuth: true}
    },
    {
        path: "/landingpage",
        name: "landingpage",
        component: LandingPage,
        meta: { requiresAuth: true},
        children: [
            {
                path: "/explore",
                name: "explore"
            },
            {
                path: "/inbox",
                name: "inbox"
            },
            {
                path: "/analyze",
                name: "analyze"
            },
            {
                path: "/share",
                name: "share"
            },
            {
                path: "/report",
                name: "report"
            },
            {
                path: "/content",
                name: "content"
            },
        ]
    },
    {
        path: "/interactions",
        name: "interactions",
        meta: { requiresAuth: true},
        component: InteractionsPage,
        children: [
            {
                path: "chat",
                name: "chat"
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes 
})

// Hiermit wird sichergestellt, dass nur authentifizierte Nutzer auf die wichtigen Seiten zugreifen können
router.beforeEach((to, from, next) => {
    
    const authStore = useAuthStore();
    if(to.matched.some(r =>  r.meta.requiresAuth)) {
        if(!authStore.isAuthenticated()) {
            console.log("not authenticated")
            next("/");
        } else {
            console.log("authenticated")
            next()
        }
    } else if (to.path === "/" && authStore.isAuthenticated()){
        console.log("umleitung zum dashboard")
        //next("/dashboard")
    } else {
        console.log("default")
        next()
    }
})

export default router