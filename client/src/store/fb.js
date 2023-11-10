import { defineStore } from "pinia";
import { inject, ref } from "vue"
import "bootstrap"

export const useFBStore = defineStore('fb', () => {
    const pages = ref([])
    const comments = ref([])
    const initFinished = ref(false)

    const axios = inject('AXIOS_INSTANCE')

    function populateData() {
        pages.value = []
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
        
        comments.value.forEach((c) => {
            c.sort((a, b) => {
                a = new Date(a);
                b = new Date(b);
                (a.timestamp > b.timestamp) ? 1 : ((b.timestamp > a.timestamp) ? -1 : 0)
            })
        })
    }

    function sendAuthTokens() {
        FB.getLoginStatus((res) => {
            axios.post("token?token="+res.authResponse.accessToken)
        })
    }

    function postReplyToComment(commentId, comment) {
        FB.api("/" + commentId + "/replies", "POST", {
            "message": comment
        }, (res) => {
            if(res && !res.error) {
                console.log("erfolgreich gepostet")
                populateData()
            }
        })
    }

    function deleteComment(commentID) {
        FB.api("/" + commentID, "DELETE", (res) => {
            if(res && !res.error) {
                console.log("erfolgreich gelöscht")
                populateData()
            }
        })
    }

    return {
        initFinished, 
        pages,
        comments, 
        populateData,
        sendAuthTokens,
        postReplyToComment,
        deleteComment
    }
})