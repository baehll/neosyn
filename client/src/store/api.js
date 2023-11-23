import { defineStore } from "pinia";
import { ref, inject } from "vue";
import { useRouter } from "vue-router";
import "bootstrap"

export const useAPIStore = defineStore("api", () => {
    const fastReplies = ref([])

    const axios = inject("AXIOS_INSTANCE");

    async function updateFastReplies(comment) {
        //currentCommentID.value = comment.id
        let res = await axios.post("/api/fast_response", {"comment": comment.text})
        fastReplies.value = res.data.answers;
        const modal = new bootstrap.Modal("#fastReplyModal")
        modal.show()
    }

    return {
        fastReplies,
        updateFastReplies
    }
})