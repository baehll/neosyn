<template>
    <div class="row">
        <NeosynBrand></NeosynBrand>
    </div>
    <div class="row">
        <div class="col login-container">
            <h4 class="text-center mb-4">Login</h4>
            <form class="row">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
            <div class="row">
                <!--
                <div class="col">
                    <a>Forgot password?</a>
                </div>
                <div class="col">
                    <p>Don't have an account yet? <a>Register now!</a></p>
                </div>
                -->
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, inject } from "vue"
import NeosynBrand from '../components/NeosynBrand.vue';


</script>

<style scoped>
    .login-container {
      max-width: 400px;
      margin: auto;
      margin-top: 100px;
    }
</style>