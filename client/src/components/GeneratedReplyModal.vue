<template>
    <div class="modal fade" tabindex="-1" id="generatedReplyModal" aria-labelledby="generatedReplyModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Generiertes Kommentar</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Schließen"></button>
                </div>
                <div class="modal-body">
                    <!---->
                    <textarea v-model="responseText" class="" rows="5" cols="48"></textarea>
                    <!---->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn" data-bs-dismiss="modal" aria-label="Schließen">Schließen</button>
                    <button type="button" class="btn" data-bs-dismiss="modal" @click="send">Senden</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAPIStore } from "../store/api"
import { useFBStore } from "../store/fb";

const fbStore = useFBStore()
const apiStore = useAPIStore()
const responseText = ref("")

watch(() => apiStore.generatedReply.text, (newValue) => {
    responseText.value = newValue;
});

function send() {    
    fbStore.replyToComment(apiStore.generatedReply.parent, apiStore.generatedReply.text)
}

onMounted(() => {
    responseText.value = apiStore.generatedReply.text
})
</script>

<style>

</style>