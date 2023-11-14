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
import { reactive } from "vue";

const fbStore = useFBStore();

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