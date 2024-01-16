<template>
        <div class="card border border-5 mb-4 p-2">
            <div class="row no-gutters">
                <div class="col-md-4 ">
                    <template v-if="post_obj.media_type === 'IMAGE'">
                        <div class="center-image">
                            <img :src="post_obj.media_url" class="img-fluid border border-2 "/>
                        </div>
                    </template>
                    <template v-else-if="post_obj.media_type === 'CAROUSEL_ALBUM'">
                        <div :id="'id_'+post_obj.id" class="carousel slide">
                            <div class="carousel-inner">
                                <template v-for="child, i in post_obj.children.data">
                                    <div class="carousel-item" :class="(i == 0) ? 'active': ''">
                                        <div class="center-image">
                                            <img :src="child.media_url" class="img-fluid border border-2"/>
                                        </div>
                                    </div>
                                </template>
                            </div>  
                            <button class="carousel-control-prev" type="button" :data-bs-target="'#id_' + post_obj.id" data-bs-slide="prev">
                                <span class="fa-solid fa-chevron-left bg-light rounded-5 p-2" aria-hidden="true" style="color: black;width: 2em; height: 2em;"></span>
                                <span class="visually-hidden">Previous</span>
                            </button>
                            <button class="carousel-control-next" type="button" :data-bs-target="'#id_' + post_obj.id" data-bs-slide="next">
                                <span class="fa-solid fa-chevron-right bg-light rounded-5 p-2" aria-hidden="true" style="color: black;width: 2em; height: 2em;"></span>
                                <span class="visually-hidden">Next</span>
                            </button>
                        </div>
                    </template>
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <div class="card-text">
                            <div class="col text-start comment-list ">
                                <div class="row">
                                    <div class="card-title">
                                            <p>
                                                <i class="fa-solid fa-thumbs-up"></i> {{ post_obj.like_count > 0 ? post_obj.like_count : "0" }}
                                                <i class="fa-solid fa-comment"></i> {{ post_obj.comments_count }}
                                            </p>
                                        <h5>{{ post_obj.caption }}</h5>
                                        <small>{{ post_obj.username }} - {{ dateFormatter(new Date(post_obj.timestamp)) }} </small>
                                    </div>
                                </div>
                                <template v-if="post_obj.comments_count != 0">
                                    <div class="card mt-3 p-1 border-1" style="min-height: 200px;">
                                        <div class="card-body" style="max-height:400px;overflow-y: auto;">
                                            <template v-for="c in post_obj.comments">
                                                <div class="card-text">
                                                    <Comment :comment="c" :shallow="false" class="" @generate-reply="generateReplyWithContext"/>
                                                    <template v-if="c?.replies != null">
                                                        <div class="card mt-3 p-1">
                                                            <div class="card-body">
                                                                <template v-for="r in c.replies.data" :key="r.id">
                                                                    <div class="card-text">
                                                                        <Comment :comment="r" :shallow="false" @generate-reply="generateReplyWithContext"/>
                                                                    </div>
                                                                </template>
                                                            </div>
                                                        </div>
                                                    </template>
                                                </div>
                                            </template>
                                        </div>
                                    </div>
                                </template>
                                <template v-else>
                                    <small>Keine Kommentare vorhanden</small>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>

<script setup>
import { useAPIStore } from '../store/api';
import { useFBStore } from '../store/fb';
import { dateFormatter } from '../utils';
import Comment from './Comment.vue';

const props = defineProps(["post_obj"])
const fbStore = useFBStore();
const apiStore = useAPIStore();

function generateReplyWithContext(commentText, targetId) {
    apiStore.setContext(props.post_obj.id, props.post_obj.media_url, props.post_obj.caption, commentText);
    apiStore.generateResponseWithContext(targetId)
}


</script>

<style scoped>

.pic {
    max-width: 907px;
    max-height: 907px;
}

.center-image {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
    }
</style>