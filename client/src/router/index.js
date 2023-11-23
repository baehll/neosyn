import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from "../views/landingpage/LandingPage.vue"
import Login from "../views/Login.vue"
import Dashboard from "../views/landingpage/children/Dashboard.vue"
import InteractionsPage from "../views/interactions/InteractionsPage.vue"

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "Dashboard",
            component: Dashboard
        },
        {
            path: "/landingpage",
            name: "landingpage",
            component: LandingPage,
            children: [
                {
                    path: "/",
                    name: "dashboard",
                    component: Dashboard
                },
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
            component: InteractionsPage,
            children: [
                {
                    path: "chat",
                    name: "chat"
                }
            ]
        },
        {
            path: "/login",
            name: "login",
            component: Login
        }
    ]
})

export default router