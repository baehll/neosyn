<template>
    <div class="modal fade" tabindex="-1" id="fastReplyModal" aria-labelledby="fastReplyModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Generierte Kommentare</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Schließen"></button>
                </div>
                <div class="modal-body">
                    <!---->
                    <fieldset>
                        <legend>Bitte Wähle eine Antwort:</legend>
                        <template v-for="answer, index in apiStore.fastReplies.replies">
                            <div class="form-check">
                                <input type="radio" class="form-check-input" :id="'answer'+index" v-model="pick" name="answers" :value="answer">
                                <label :for="'answer'+index" class="form-check-label">{{ answer }}</label>
                            </div>
                        </template>
                    </fieldset>
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
import { ref } from "vue";
import { useAPIStore } from "../store/api"
import { useFBStore } from "../store/fb";

const apiStore = useAPIStore()
const fbStore = useFBStore();
const pick = ref("")

function send() {
    fbStore.replyToComment(apiStore.fastReplies.targetId, pick.value)

}
</script>

<style>

</style>