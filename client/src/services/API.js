import axios from "axios";

export const client = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true
});

client.interceptors.request.use(
    function (config) {
        return config;
    },
    function (error) {
        return Promise.reject(error.response);
    }
);

/*
 * Add a response interceptor
 */
client.interceptors.response.use(
    response => {
        return response;
    },
    function (error) {
//        store.dispatch('Alert/showError', {
//            message: error.response.data.message
//        });
        return Promise.reject(error.response);
    }
);
