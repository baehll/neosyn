<template>
    <div class='d-flex row border border-2 flex-nowrap'>
        <div class="col-2 ps-0">
            <img :src="state.profile_picture_url" class="profile-picture"/>
            <!--Profile picture-->
        </div>
        <div class="col-10">
            <div class="row">
                <div class="col">
                    <b>{{ comment.username }}</b>
                </div>
                <div class="col-1">

                </div>
                <div class="col">
                    {{ state.time }}
                </div>
            </div>
            <div class="row mb-1">
                <div class="divider ">

                </div>
            </div>
            <div class="row">
                <p>
                    {{ comment.text }}
                </p>
            </div>
            <div class="row mb-1">
                <div class="divider">

                </div>
            </div>
            <div class="row">
                <div class="col-auto">
                    <button class="btn disabled">Reply</button>
                </div>
                <div class="col-auto">
                    <button @click="fastReply" class="btn btn-primary">Fast Reply</button>
                </div>
                <div class="col-auto">
                    <button @click="fbStore.deleteComment(props.comment.id)" class="btn btn-primary">Delete</button>
                </div>
            </div>
        </div>
        <FastReplyModal :picked="state.picked" @send="sendComment"/>
    </div>
</template>

<script setup>
import { inject, onMounted, reactive } from 'vue';
import FastReplyModal from "./FastReplyModal.vue"
import { useAPIStore } from "../store/api"
import { useFBStore } from '../store/fb';
 
const apiStore = useAPIStore()
const fbStore = useFBStore()
const props = defineProps(['comment'])
const state = reactive({
    profile_picture_url: "",
    time: "",
    picked: ""
})

async function fastReply() {
    apiStore.updateFastReplies(props.comment)
}    

function sendComment(val) {
    fbStore.postReplyToComment(props.commment.id, val)
    state.picked = ""
}

onMounted(() => {
    //console.log(props.comment)
    FB.api(props.comment.from.id, {fields:"profile_picture_url"}, (res) => {
        state.profile_picture_url = res.profile_picture_url;
    })
    const d = new Date(props.comment.timestamp)
    state.time = `${formatNumbers(d.getDay())}.${formatNumbers(d.getMonth())}.${d.getFullYear()}, ${formatNumbers(d.getHours())}:${formatNumbers(d.getMinutes())}`;
})

function formatNumbers(i) {
    return i.toString().padStart(2, "0")
}

</script>

<style>
.profile-picture {
    max-width: 4em;
    max-height: 4em;
    border-radius: 100%;
}
.divider {
    height: 0.3em;
    background-color: rgb(170, 170, 170);
}
</style>