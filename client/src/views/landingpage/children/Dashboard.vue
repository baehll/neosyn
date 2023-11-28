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
                    <ul class="list-group list-group-flush" v-for="pageComments in fbStore.comments">
                        <div v-for="c in pageComments">
                            <Comment :comment="c" :actions_enabled="true" class="list-group-item rounded-4 p-3 m-1 shadow-lg" />
                            <template v-for="r in c.replies?.data">
                                <Comment :comment="r" :actions_enabled="true" class="list-group-item rounded-4 p-3 m-1" />
                            </template>
                        </div>
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

const fbStore = useFBStore();

onMounted(() => {
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
            fbStore.populateData();
        } else {
            authUser();
            fbStore.populateData();
        }
    }
    /*  
    console.log("timing test")
    if(!fbStore.initFinished) {
        console.log("test1")
        fbStore.loginToFB();
        console.log("1store angeblich geladen,  " + fbStore.pages.length)
    } else {
        console.log("2store angeblich geladen,  " + fbStore.pages.length)
    }
    */
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