import axios from "axios";
import store from '../store';

let client

const apiClient = () => {
    client = axios.create({
        baseURL: process.env.VITE_BASE_API_URL
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
            store.dispatch('Alert/showError', {
                message: error.response.data.message
            });
            return Promise.reject(error.response);
        }
    );

    return client
}
