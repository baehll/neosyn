import { defineStore } from "pinia";
import {ref} from "vue"

export const useFBStore = defineStore('fb', () => {
    const name = ref("");

    function populateData() {
        FB.api("/me", (res) => {
            console.log("hallo " + res.name)
            name.value = res.name;
        })

    }

    return { name, populateData }
})