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
                            <Comment :comment="c" class="list-group-item rounded-4 p-3 m-1 shadow-lg" />
                            <template v-for="r in c.replies?.data">
                                <Comment :comment="r" class="list-group-item rounded-4 p-3 m-1" />
                            </template>
                        </div>
                    </ul>
                </div>
            </div>
            <!--
            <div class="col">
                <template v-for="page in fbStore.pages">
                    <div class="row border border-5">
                        <h3>{{ page.name }}</h3>
                        <template v-for="media in page.media_objs">
                            <div class="border border-5">
                                <template v-if="media.media_type === 'IMAGE'">
                                    <img :src="media.media_url" class="border border-2"/>
                                </template>
                                <div class="text-start border border-5">
                                    <h3>
                                        {{ media.caption }}
                                    </h3>
                                    <template v-for="c in media.comments.data">
                                        <Comment :comment="c" class="border border-3"/>
                                        <template v-for="r in c.replies.data">
                                            <Comment :comment="r" class="ms-4 border border-3"/>
                                        </template>
                                    </template>
                                </div>
                            </div>
                        </template>
                    </div>
                </template>
            </div>
            -->
        </div>
    </div>
</template>

<script setup>
import { useFBStore } from "../../../store/fb"
import Comment from '../../../components/Comment.vue'
import { reactive } from "vue";

const fbStore = useFBStore();

</script>

<style scoped>
.comment-list {
    max-height: 60vh;
}

.comment-list-body {
    overflow-y: auto;
    overflow-x: hidden;
}
</style>