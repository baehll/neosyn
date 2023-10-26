<template>
    <div>
        <div class="row">
            <h1>Dashboard!</h1>
        </div>
        <div class="row">
            <template v-if="store.name != ''">
                <div>
                    <h4>Hallo, {{ store.name }}</h4>
                </div>
            </template>
            <div class="col">
                <template v-for="page in store.pages">
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
                                    <template v-for="comment in media.comments.data">
                                        <div class="border border-5">
                                            <b>{{ comment.username }}</b> {{ comment.text }}
                                        </div>
                                        <template v-for="reply in comment.replies.data">
                                            <div class="ms-4 border border-5 ">
                                                <b>{{ reply.username }}</b> {{ reply.text }}
                                            </div>
                                        </template>
                                    </template>
                                </div>
                            </div>
                        </template>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';
import {useFBStore} from "../../../store/fb"

const store = useFBStore();

onMounted(() => {
    
})

</script>

<style scoped>

</style>