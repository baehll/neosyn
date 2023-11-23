<template>
    <div class="row">
        <div class="col login-container">
            <h4 class="text-center mb-4">Login</h4>
            <form class="row" @submit.prevent="login">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" name="username" v-model="username" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="password" v-model="password" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, inject, nextTick } from "vue"
import { useAuthStore } from "../store/auth"
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();
const username = ref("");
const password = ref("");

if (authStore.isAuthenticated) {
  router.push('/dashboard');
}

async function login() {
    await authStore.login(username.value, password.value)
    nextTick(() => {
        router.push({name: "Dashboard"})
    })
}
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: auto;
    margin-top: 100px;
}
</style>