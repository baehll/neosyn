<template>
    <div class="container">    
        <div v-if="authStore.authenticated" >
            <TopNavbar></TopNavbar>
            <SideNavbar></SideNavbar>
            <GeneratedReplyModal></GeneratedReplyModal>
            <FastReplyModal></FastReplyModal>
        </div>
        <LoadingScreenModal></LoadingScreenModal>
        <div class=" mt-4">
            <router-view></router-view>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import FastReplyModal from './components/FastReplyModal.vue';
import GeneratedReplyModal from './components/GeneratedReplyModal.vue';
import LoadingScreenModal from './components/LoadingScreenModal.vue';
import SideNavbar from './components/SideNavbar.vue';
import TopNavbar from './components/TopNavbar.vue';
import { useAuthStore } from './store/auth';
import { useGeneralStore } from './store/general';

const authStore = useAuthStore();
const generalStore = useGeneralStore();

onMounted(() => {
    generalStore.initInfoModal();
})
</script>

<style scoped>

</style>
