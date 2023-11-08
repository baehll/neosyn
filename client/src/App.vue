<template>
    <!-- Side Nav Bar-->
    <div class="">
        <SideNavbar></SideNavbar>
    </div>
    <!-- main body -->
    <div class="container">
        <Dashboard></Dashboard>
        <!--<router-view></router-view>-->
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import NeosynBrand from './components/NeosynBrand.vue';
import Dashboard from "./views/landingpage/children/Dashboard.vue"
import SideNavbar from './components/SideNavbar.vue';


</script>

<style scoped>

</style>
