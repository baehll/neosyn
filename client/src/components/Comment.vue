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
                <p>
                    {{ (comment.like_count != null) ? comment.like_count : 0 }} <i class="fa-solid fa-thumbs-up"></i>
                </p>
            </div>
            <div class="row mb-1">
                <div class="divider">

                </div>
            </div>
            <div class="row">
                <div class="col-auto">
                    <button @click="sendReply" class="btn btn-primary" :class="{'disabled': props.shallow}">Reply</button>
                </div>
                <div class="col-auto">
                    <button @click="fastReply" class="btn btn-primary">Fast Reply</button>
                </div>
                <div class="col-auto">
                    <button @click="fbStore.deleteComment(props.comment.id)" class="btn btn-primary">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { inject, onMounted, reactive } from 'vue';
import { useAPIStore } from "../store/api"
import { useFBStore } from '../store/fb';
import {dateFormatter} from '../utils';
 
const apiStore = useAPIStore()
const fbStore = useFBStore()
const emit = defineEmits(['generate-reply'])
const props = defineProps(['comment', 'shallow'])

const state = reactive({
    profile_picture_url: "",
    time: "",
    picked: ""
})

async function fastReply() {
    apiStore.updateFastReplies(props.comment.text, props.comment.id)
}    

async function sendReply() {
    emit("generate-reply", props.comment.text, props.comment.id)
}

onMounted(() => {
    //console.log(props.comment)
    FB.api(props.comment.from.id, {fields:"profile_picture_url"}, (res) => {
        state.profile_picture_url = res.profile_picture_url;
    })
    state.time = dateFormatter(new Date(props.comment.timestamp));
})


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