<template>
    <div class="container">    
        <div v-if="authStore.authenticated" >
            <TopNavbar></TopNavbar>
            <SideNavbar></SideNavbar>
            <GeneratedReplyModal></GeneratedReplyModal>
            <FastReplyModal></FastReplyModal>
        </div>
        <div class=" mt-4">
            <router-view></router-view>
        </div>
    </div>
</template>

<script setup>
import FastReplyModal from './components/FastReplyModal.vue';
import GeneratedReplyModal from './components/GeneratedReplyModal.vue';
import SideNavbar from './components/SideNavbar.vue';
import TopNavbar from './components/TopNavbar.vue';
import { useAuthStore } from './store/auth';
import { reactive } from 'vue';

const authStore = useAuthStore()
</script>

<style scoped>

</style>
