<template>
    <div class="container">    
        <div v-if="authStore.isAuthenticated" >
            <TopNavbar></TopNavbar>
            <SideNavbar></SideNavbar>
        </div>
        <div class=" mt-4">
            <router-view></router-view>
        </div>
    </div>
</template>

<script setup>
import SideNavbar from './components/SideNavbar.vue';
import TopNavbar from './components/TopNavbar.vue';
import { useAuthStore } from './store/auth';

const authStore = useAuthStore()
</script>

<style scoped>

</style>
