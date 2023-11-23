import { defineStore } from 'pinia'
import { ref, inject } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const isAuthenticated = ref(localStorage.getItem("token") != null)

    const axios = inject("AXIOS_INSTANCE");

    async function login(un, pw) {
        try {
            let res = await axios.post("/auth/login", {
                username: un,
                password: pw
            })
    
            let token = res.data.token;
            localStorage.setItem('token', token)
            isAuthenticated.value = true

        } catch (error) {
            console.error("Login failed", error)
        }
    }

    function logout() {

    }

    return {
        isAuthenticated,
        login,
        logout
    }
})