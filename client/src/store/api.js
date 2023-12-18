import { defineStore } from "pinia";
import { ref, inject } from "vue";
import { useRouter } from "vue-router";
import "bootstrap"
import { useGeneralStore } from "./general";

export const useAPIStore = defineStore("api", () => {
    const fastReplies = ref({
        replies: [],
        targetId: ""
    })

    const generatedReply = ref({
        parent: "",
        text: ""
    })
    
    const replyContext = ref({
        id: "",
        media_url: "",
        caption: "",
        comment: ""
    })

    const axios = inject("AXIOS_INSTANCE");
    const gnStore = useGeneralStore();

    function setContext(id, media_url, caption, comment = "") {
        replyContext.value.id = id;
        replyContext.value.media_url = media_url;
        replyContext.value.caption = caption;
        if(comment == "") {
            replyContext.value.comment = "";
        } else {
            replyContext.value.comment = comment;
        }
    }

    async function getLongLivedToken(){
        FB.getLoginStatus(async (res) => {
            if(res && res.authResponse) {
                try {
                    let resp = await axios.post("/api/long_lived_access", {access_token: res.authResponse.accessToken})
                    //Antwort ist ein Code, um weiter zu querien
                    if(resp) {
                        let tokenRes = await axios.get("https://graph.facebook.com/v18.0/oauth/access_token", {
                            "code": resp.data.code,
                            "client_id": import.meta.env.VITE_FB_APP_ID,
                            "redirect_uri": "https://quiet-mountain-69143-51eb8184b186.herokuapp.com/"
                        })

                        if(tokenRes) {
                            let body = {
                                machine_id : tokenRes.data.machine_id,
                                access_token: tokenRes.data.access_token,
                                platform: "GraphAPI"
                            }

                            //Ablaufzeitpunkt des Tokens berechnen, wenn einer mitgegeben wurde
                            if (tokenRes.data.expires_in != null) {
                                let expirationDate = new Date(new Date().getTime() + tokenRes.data.expires_in * 1000)
                                body.expiration = expirationDate
                            } else {
                                body.expirationDate = ""
                            }
                            let serverRes = await axios.post("/api/long_lived_client_token", body)
                        }
                    }
                } catch (error) {
                    console.error("Error while sending FB Token to server, " + error)
                }
            }
        })
        
    }

    async function updateFastReplies(commentText, commentId) {
        try {
            gnStore.showLoadingScreen()

            let res = await axios.post("/api/fast_response", {"comment": commentText})
            fastReplies.value.replies = res.data.answers;
            fastReplies.value.targetId = commentId;

            gnStore.hideLoadingScreen()
            const modal = new bootstrap.Modal("#fastReplyModal")
            modal.show()
        } catch (error) {
            console.log("Error while fetching quick responses, " + error)
        } finally {
            if(gnStore.infoModalActive) gnStore.hideLoadingScreen();
        }

    }

    async function generateResponseWithContext(targetId) {
        try {
            gnStore.showLoadingScreen();

            let res = await axios.post("/api/context_response", replyContext.value);
            generatedReply.value.parent = targetId;
            generatedReply.value.text = res.data.answer;

            gnStore.hideLoadingScreen();
            
            const modal = new bootstrap.Modal("#generatedReplyModal");
            modal.show();
        } catch (error) {
            console.error("Error when requesting Respone with Context", error)
        } finally {
            if(gnStore.infoModalActive) gnStore.hideLoadingScreen();
        }
    }

    return {
        fastReplies,
        generatedReply,
        updateFastReplies,
        generateResponseWithContext,
        setContext,
        sendFBToken
    }
})