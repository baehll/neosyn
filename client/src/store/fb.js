import { defineStore } from "pinia";
import {ref} from "vue"

export const useFBStore = defineStore('fb', () => {
    const name = ref("");
    const pages = ref([])

    function populateData() {
        FB.api("/me", (res) => {
            name.value = res.name;
        })

        FB.api("/me/accounts", (resp) => {
            //console.log(res);
            //pages.value = res.data;

            resp.data.forEach(e => {
                let currentPage = { name: e.name }
                FB.api(e.id, {fields: 'instagram_business_account'}, (res) => {
                    currentPage.acc = res.instagram_business_account.id;
                    
                    FB.api(currentPage.acc + "/media", {fields: 'caption,id,like_count,media_type,media_url,timestamp,username,comments_count,comments{text, username, replies{username, text}}'}, (r) => {
                        //console.log(r)
                        currentPage.media_objs = r.data
                    })
                })
                pages.value.push(currentPage);
            });
            console.log(pages.value)
        })
    }


    return { 
        name,
        pages, 
        populateData 
    }
})