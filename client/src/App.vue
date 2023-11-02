<template>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <NeosynBrand></NeosynBrand>
            <button class="navbar-toggler" type="button" data-bs-toggle="collaps" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
            </div>
        </div>
    </nav>
    <div class="container">
        <Dashboard></Dashboard>
        <!--<router-view></router-view>-->
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import NeosynBrand from './components/NeosynBrand.vue';
import Dashboard from "./views/landingpage/children/Dashboard.vue"
import NeosynBrand from './components/NeosynBrand.vue';

</script>

<style scoped>

</style>
