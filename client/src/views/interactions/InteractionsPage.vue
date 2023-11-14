<template>
    <div class="col">
        <template v-for="page in fbStore.pages">
            <div class="row">
                <b>Posts für</b> <h3>{{ page.name }}</h3>
                <template v-for="media in page.media_objs">
                    <IGPost style="min-width: 85vw;" :post_obj="media" />
                </template>
            </div>
        </template>
    </div>
</template>

<script setup>
import IGPost from '../../components/IGPost.vue';
import { useFBStore } from '../../store/fb';

const fbStore = useFBStore()
</script>