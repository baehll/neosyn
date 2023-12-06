import { defineStore } from "pinia";
import { inject, ref } from "vue"
import "bootstrap"
import { useGeneralStore } from "./general"

export const useFBStore = defineStore('fb', () => {
    const pages = ref([])
    const comments = ref([])
    const initFinished = ref(false)

    const axios = inject('AXIOS_INSTANCE')
    const gnStore = useGeneralStore();

    function populateData() {
        pages.value = []
        initFinished.value = false
        comments.value = []

        //Zuerst alle zugehörigen Pages/Accounts finden
        FB.api("/me/accounts", (resp) => {
            //über jede Page iterieren
            resp.data.forEach(e => {
                let currentPage = { name: e.name }
                //von jeder gemanagten Page den business account nehmen
                FB.api(e.id, {fields: 'instagram_business_account'}, (res) => {
                    currentPage.acc = res.instagram_business_account.id;
                    //von jedem business account alle zugehörigen posts + comments + comment_replies sammeln
                    FB.api(currentPage.acc + "/media", {fields: 'caption,id,like_count,media_type,media_url,timestamp,username,comments_count,comments,children{media_url}'}, (r) => {
                        //console.log(r)
                        currentPage.media_objs = r.data

                        //r.data sind alle medien, die auf einem Business Account sind, die jeweils ihre eigenen Kommentare haben
                        for(let key in r.data) {
                            let post = r.data[key]
                            if(post.comments_count > 0) {
                                FB.api(post.id + "/comments", {fields: "from, text, username, timestamp, parent, like_count,replies{from, parent, timestamp, username, text}"}, (commentRes) => {
                                    comments.value.push(commentRes.data)
                                    currentPage.media_objs[key].comments = commentRes.data
                                })
                            }
                        }
                    })
                })
                pages.value.push(currentPage);
            });
        })
        //Nach Zeitstempel sortieren
        comments.value.forEach((c) => {
            c.sort((a, b) => {
                a = new Date(a);
                b = new Date(b);
                (a.timestamp > b.timestamp) ? 1 : ((b.timestamp > a.timestamp) ? -1 : 0)
            })
        })
        
        initFinished.value = true;
        
    }

    function sendAuthTokens() {
        FB.getLoginStatus((res) => {
            axios.post("token?token=" + res.authResponse.accessToken)
        })
    }

    function replyToComment(commentId, comment) {
        try {
            gnStore.showLoadingScreen();
            FB.api("/" + commentId + "/replies", "POST", {
                "message": comment
            }, (res) => {
                if(res && !res.error) {
                    gnStore.hideLoadingScreen();
                    populateData();
                }
            })
        } catch (error) {
            console.error("Error while replying to comment\n", error)
        } finally {
            gnStore.hideLoadingScreen();
        }
    }

    function replyToObject(id, message) {
        try {
            gnStore.showLoadingScreen();

            FB.api("/" + id + "/comments", "POST", {
                "message": message
            }, (res) => {
                if(res && !res.error) {
                    gnStore.hideLoadingScreen();
                    populateData();
                }
            })
        } catch (error) {
            console.error("Error while replying to object\n",error)
        } finally {
            gnStore.hideLoadingScreen();
        }
    }

    function deleteComment(commentID) {
        try {
            gnStore.showLoadingScreen();
            FB.api("/" + commentID, "DELETE", (res) => {
                if(res && !res.error) {
                    gnStore.hideLoadingScreen();
                    populateData();
                }
            })
        } catch (error) {
            console.error("Error while deleting comment\n",error)
        } finally {
            gnStore.hideLoadingScreen();
        }
        
        
    }


    return {
        initFinished, 
        pages,
        comments, 
        populateData,
        sendAuthTokens,
        replyToComment,
        deleteComment,
        replyToObject
    }
})