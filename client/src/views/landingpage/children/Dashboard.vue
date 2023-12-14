<template>
    <div>
        <div class="row">
            <h1>Dashboard</h1>
        </div>
        <div class="row">
            <div class="card p-0 comment-list">
                <div class="card-header bg-white">
                    <h3>Recent Comments</h3>
                    <button type="button" class="btn" @click="fbStore.populateData()">
                        <i class="fa-solid fa-repeat"></i>
                    </button>
                </div>
                <div class="card-body comment-list-body">
                    <ul class="list-group list-group-flush" v-show="isReady">
                        <template v-for="page in fbStore.pages">
                            <template v-for="post in page.media_objs">
                                <template v-for="comment in post.comments" :key="comment.id">
                                    <li class="list-group-item border-0" >
                                        <Comment :comment="comment" :shallow="true" class="list-group-item rounded-4 p-3 m-1 shadow-lg" />
                                    </li>
                                    <template v-for="reply in comment.replies?.data" :key="reply.id">
                                        <li class="list-group-item border-0">
                                            <Comment :comment="reply" :shallow="true" class="list-group-item rounded-4 p-3 m-1 shadow-lg" />
                                        </li>
                                    </template>
                                </template>
                            </template>
                        </template>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useFBStore } from "../../../store/fb"
import Comment from '../../../components/Comment.vue'
import { inject, onBeforeMount, onMounted} from "vue";
import { useAPIStore } from "../../../store/api";

const fbStore = useFBStore();
const apiStore = useAPIStore();

function isReady() {
    return fbStore.initFinished;
}

onBeforeMount(() => {
    try {
        FB.init({
            appId: import.meta.env.VITE_FB_APP_ID,
            version: "v18.0",
            xfbml: true,
            status: true,
            cookie: true,
        });
        
        // Check if the current user is logged in and has authorized the app
        FB.getLoginStatus(checkLoginStatus);
        
        // Login in the current user via Facebook and ask for email permission
        function authUser() {
            FB.login(checkLoginStatus, {scope: 'pages_show_list,business_management,instagram_basic,instagram_manage_comments,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_engagement,public_profile'});
        }
        
        // Check the result of the user status and display login button if necessary
        function checkLoginStatus(response) {
            if(response && response.status == 'connected') {
                if(!fbStore.initFinished) fbStore.populateData();
            } else {
                authUser();
                fbStore.populateData();
            }
        }
    } catch (error) {
        console.error("Error while trying to setup FB JDK\n" + error)
    }   
})

</script>

<style scoped>
.comment-list {
    max-height: 80vh;
}

.comment-list-body {
    overflow-y: auto;
    overflow-x: hidden;
}
</style>