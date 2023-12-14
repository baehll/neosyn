import { defineStore } from 'pinia'
import { ref, inject, computed } from 'vue'
import { useRouter } from "vue-router";
import { parseJwt } from '../utils';

export const useAuthStore = defineStore('auth', () => {
    const axios = inject("AXIOS_INSTANCE");
    const router = useRouter();
    const authenticated = ref(false);
    
    /**
     * 
     * @param {*} un 
     * @param {*} pw 
     */
    async function login(un, pw) {
        try {
            let res = await axios.post("/auth/login", {
                username: un,
                password: pw
            })
    
            let token = res.data.token;
            sessionStorage.setItem('token', token);
            authenticated.value = true;

            axios.defaults.headers.common['Authorization'] = "Bearer " + token
            
        } catch (error) {
            console.error("Login failed", error)
        }
    }

    /**
     * 
     */
    async function logout() {
        try {
            let res = await axios.post("/auth/logout", {headers: [{"Content-Type" : "application/json"}]})
        } catch (error) {
            console.error("Logout failed", error)
        } finally {
            authenticated.value = false;
            sessionStorage.removeItem("token")
            router.push("/")
        }
    }

    /**
     * 
     * @returns 
     */
    function isAuthenticated() {
        if(sessionStorage.getItem("token") == null) {
            authenticated.value = false;
            return false;
        } else {
            const jwtToken = parseJwt(sessionStorage.getItem("token"));
            if(jwtToken.exp < Date.now()) {
                authenticated.value = true;
                return true;
            } else {
                authenticated.value = false;
                return false;
            }
        } 
    }

    return {
        authenticated,
        isAuthenticated,
        login,
        logout
    }
})