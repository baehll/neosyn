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
            <template v-if="props.actions_enabled">
                <div class="row mb-1">
                    <div class="divider">

                    </div>
                </div>
                <div class="row">
                    <div class="col-auto d-flex justify-content-center align-items-center">
                        <button class="mx-1 btn disabled">Reply</button>
                        <button @click="fastReply" class="mx-1 btn btn-primary">Fast Reply</button>
                        <button @click="fbStore.deleteComment(props.comment.id)" class="mx-1 btn btn-primary">Delete</button>
                    </div>
                </div>
            </template>
        </div>
        <template v-if="props.actions_enabled">
            <Fastreplymodal :picked="state.picked" @send="sendComment"/>
        </template>
    </div>
</template>

<script setup>
import { inject, onMounted, reactive } from 'vue';
import { useAPIStore } from "../store/api"
import { useFBStore } from '../store/fb';
import utils from '../utils';
import Fastreplymodal from './FastReplyModal.vue';
 
const apiStore = useAPIStore()
const fbStore = useFBStore()
const props = defineProps(['comment', 'actions_enabled'])
const state = reactive({
    profile_picture_url: "",
    time: "",
    picked: ""
})

async function fastReply() {
    apiStore.updateFastReplies(props.comment)
}    

function sendComment(val) {
    fbStore.postReplyToComment(props.comment.id, val)
    state.picked = ""
}

onMounted(() => {
    //console.log(props.comment)
    FB.api(props.comment.from.id, {fields:"profile_picture_url"}, (res) => {
        state.profile_picture_url = res.profile_picture_url;
    })
    state.time = utils.dateFormatter(new Date(props.comment.timestamp));
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