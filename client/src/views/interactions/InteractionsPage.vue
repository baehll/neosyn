<template>
    <div class="col">
        <b>Posts für</b>
        <p>
            <select v-model="selected">
                <option disabled>IG Seite auswählen</option>
                <template v-for="page, index in fbStore.pages">
                    <option :value="index">{{ page.name }}</option>
                </template>
            </select>
        </p>
        <div class="row" v-if="fbStore.initFinished">
            <template v-for="media in fbStore.pages[selected].media_objs">
                <IGPost style="max-height: fit-content;" :post_obj="media" />
            </template>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import IGPost from '../../components/IGPost.vue';
import { useFBStore } from '../../store/fb';

const selected = ref(0)

const fbStore = useFBStore()
</script>