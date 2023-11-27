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
const app_id = inject("VITE_FB_APP_ID");

const initFacebook = () => {
    return new Promise((resolve, reject) => {
        window.fbAsyncInit = function () {
            FB.init({
            appId: app_id,
            xfbml: true,
            version: 'v18.0',
            status: true
            });

            // Hier kannst du zusätzliche Anpassungen vornehmen, wenn nötig

            FB.Event.subscribe('auth.statusChange', () => {
            FB.getLoginStatus((fbRes) => {
                if(fbRes && fbRes.status !== 'connected') {
                    FB.login((res) => {
                        if(res.authResponse) {
                            fbStore.populateData()
                        }
                    }, {scope: 'pages_show_list,business_management,instagram_basic,instagram_manage_comments,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_ads,pages_manage_engagement,public_profile'})
                } else {
                    fbStore.populateData()
                }
            })
        })
            resolve(); // Resolviere das Promise, wenn die Initialisierung abgeschlossen ist
        };
  });
}

onMounted(() => {
    if(!fbStore.initFinished) {
        initFacebook().then(() => {
            fbStore.populateData();
        });

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