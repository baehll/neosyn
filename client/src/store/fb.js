import { defineStore } from "pinia";
import {ref} from "vue"

export const useFBStore = defineStore('fb', () => {
    const pages = ref([])
    const comments = ref([])
    const initFinished = ref(false)

    function populateData() {
        //Zuerst alle zugehörigen Pages/Accounts finden
        FB.api("/me/accounts", (resp) => {
            //über jede Page iterieren
            resp.data.forEach(e => {
                let currentPage = { name: e.name }
                //von jeder gemanagten Page den business account nehmen
                FB.api(e.id, {fields: 'instagram_business_account'}, (res) => {
                    currentPage.acc = res.instagram_business_account.id;
                    //von jedem business account alle zugehörigen posts + comments + comment_replies sammeln
                    FB.api(currentPage.acc + "/media", {fields: 'caption,id,like_count,media_type,media_url,timestamp,username,comments_count,comments'}, (r) => {
                        //console.log(r)

                        currentPage.media_objs = r.data

                        //r.data sind alle medien, die auf einem Business Account sind, die jeweils ihre eigenen Kommentare haben
                        r.data.forEach(p => {
                            if(p.comments_count > 0) {
                                FB.api(p.id + "/comments", {fields: "from, text, username, timestamp, replies{from, timestamp, username, text}"}, (commentRes) => {
                                    comments.value.push(commentRes.data)
                                })
                            }
                        })
                    })
                })
                pages.value.push(currentPage);
            });
        })
        initFinished.value = true;
    }


    return {
        initFinished, 
        pages,
        comments, 
        populateData 
    }
})