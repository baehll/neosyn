<template>
    <div class="container">    
        <div class="">
            <SideNavbar></SideNavbar>
        </div>
        <router-view></router-view>
    </div>
</template>

<script setup>
import Login from "./views/Login.vue"
import SideNavbar from './components/SideNavbar.vue';

function isTokenNull() {
    return localStorage.getItem("token") == null;
}

</script>

<style scoped>

</style>
