import { defineStore } from "pinia";
import {ref} from "vue"

export const useFBStore = defineStore('fb', () => {
    const name = ref("");
    const pages = ref([])

    function populateData() {
        FB.api("/me", (res) => {
            name.value = res.name;
        })

        //Zuerst alle zugehörigen Pages/Accounts finden
        FB.api("/me/accounts", (resp) => {
            //über jede Page iterieren
            resp.data.forEach(e => {
                let currentPage = { name: e.name }
                //von jeder gemanagten Page den business account nehmen
                FB.api(e.id, {fields: 'instagram_business_account'}, (res) => {
                    currentPage.acc = res.instagram_business_account.id;
                    //von jedem business account alle zugehörigen posts + comments + comment_replies sammeln
                    FB.api(currentPage.acc + "/media", {fields: 'caption,id,like_count,media_type,media_url,timestamp,username,comments_count,comments{from, text, username, timestamp, replies{from, timestamp, username, text}}'}, (r) => {
                        currentPage.media_objs = r.data
                    })
                })
                pages.value.push(currentPage);
            });
        })
    }


    return { 
        name,
        pages, 
        populateData 
    }
})