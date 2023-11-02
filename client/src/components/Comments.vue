<template>
    <div class='row'>
        <div class="col-1 pt-2">
            <img :src="state.profile_picture_url" class="profile-picture"/>
            <!--Profile picture-->
        </div>
        <div class="col ps-4">
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
                <div class="divider ">

                </div>
            </div>
            <div class="row">
                <div class="col-auto">
                    <button>Reply</button>
                </div>
                <div class="col-auto">
                    <button>Fast Edit</button>
                </div>
                <div class="col-auto">
                    <button>Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';


const props = defineProps(['comment'])
const state = reactive({
    profile_picture_url: "",
    time:""
})

onMounted(() => {
    console.log(props.comment)
    FB.api(props.comment.from.id, {fields:"profile_picture_url"}, (res) => {
        state.profile_picture_url = res.profile_picture_url;
    })
    const d = new Date(props.comment.timestamp)
    state.time = d.getDay() + "." + d.getMonth() + "." + d.getFullYear() + ", " + d.getHours() + ":" + d.getMinutes();
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
    max-width: 90%;
    background-color: rgb(170, 170, 170);
}
</style>