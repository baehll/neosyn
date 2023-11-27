<template>
    <div class="navbar top-navbar">
        <div class="container-fluid justify-content-end">
            <button class="btn" @click="authStore.logout()">
                <i class="fa-solid fa-right-from-bracket" style="color: #ffffff;"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '../store/auth';

const authStore = useAuthStore()
</script>

<style scoped>
.top-navbar {
    top: 0;
    left: 0;
    position: fixed;
    width: 100vw;
    z-index: 998;
    background-color: #2a2a2e;
    margin-left: 0;
    color: #ffffff;
}
</style>