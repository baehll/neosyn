import { defineStore } from 'pinia'
import { ref, inject } from 'vue'
import { useRouter } from "vue-router";

export const useAuthStore = defineStore('auth', () => {
    const isAuthenticated = ref(localStorage.getItem("token") != null)

    const axios = inject("AXIOS_INSTANCE");
    const router = useRouter()

    async function login(un, pw) {
        try {
            let res = await axios.post("/auth/login", {
                username: un,
                password: pw
            })
    
            let token = res.data.token;
            localStorage.setItem('token', token)
            isAuthenticated.value = true;

            axios.defaults.headers.common['Authorization'] = "Bearer " + token
            
            console.log(axios)
        } catch (error) {
            console.error("Login failed", error)
        }
    }

    async function logout() {
        try {
            console.log(axios.defaults)
            let res = await axios.post("/auth/logout", {headers: [{"Content-Type" : "application/json"}]})
            localStorage.removeItem("token")
            isAuthenticated.value = false
            router.push("/")
        } catch (error) {
            console.error("Logout failed", error)
        }
    }

    return {
        isAuthenticated,
        login,
        logout
    }
})