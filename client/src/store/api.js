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
        setContext
    }
})