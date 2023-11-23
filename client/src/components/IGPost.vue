<template>
        <div class="border border-5 row">
            <template v-if="post_obj.media_type === 'IMAGE'">
                <div class="col-8 d-flex justify-content-center align-items-center">
                    <img :src="post_obj.media_url" class="pic border border-2"/>
                </div>
            </template>
            <template v-else-if="post_obj.media_type === 'CAROUSEL_ALBUM'">
                <div :id="'id_'+post_obj.id" class="col-8 carousel slide">
                    <div class="carousel-inner">
                        <template v-for="child, i in post_obj.children.data">
                            <div class="carousel-item" :class="(i == 0) ? 'active': ''">
                                <div class="d-flex justify-content-center align-items-center">
                                    <img :src="child.media_url" class="pic border border-2"/>
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
            <div class="col text-start comment-list ">
                <div class="row">
                    <p>
                        <b>{{ post_obj.username }} - {{ utils.dateFormatter(new Date(post_obj.timestamp)) }} </b>
                            <p>
                                <i class="fa-solid fa-thumbs-up"></i> {{ post_obj.like_count > 0 ? post_obj.like_count : "0" }}
                                <i class="fa-solid fa-comment"></i> {{ post_obj.comments_count }}
                            </p>
                    </p>
                    <h3>
                        {{ post_obj.caption }}
                    </h3>
                </div>
                <div class="row comment-list-body h-100">
                    <template v-for="c in post_obj.comments">
                        <Comment :comment="c" :actions_enabled="true" class="border border-3"/>
                        <template v-if="c?.replies != null">
                            <template v-for="r in c.replies.data">
                                <Comment :comment="r" :actions_enabled="true" class="ms-4 border border-3"/>
                            </template>
                        </template>
                    </template>
                </div>
            </div>
        </div>
</template>

<script setup>
import { useFBStore } from '../store/fb';
import utils from '../utils';
import Comment from './Comment.vue';

const props = defineProps(["post_obj"])
const fbStore = useFBStore();

</script>

<style scoped>

.pic {
    max-width: 907px;
    max-height: 907px;
}

.comment-list {
    max-height: 50vh;
}

.comment-list-body {
    overflow-y: auto;
    overflow-x: hidden;
}
</style>