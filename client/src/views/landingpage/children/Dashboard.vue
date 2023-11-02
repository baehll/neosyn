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
        </div>
    </div>
</template>

<script setup>
import { useFBStore } from "../../../store/fb"
import Comment from '../../../components/Comments.vue'

const store = useFBStore();

</script>

<style scoped>

</style>