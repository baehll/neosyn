<template>
    <div class="row">
        <NeosynBrand></NeosynBrand>
    </div>
    <div class="row">
        <div class="col">
            <h4>Login</h4>
            <div class="row">
                <input placeholder="Username" />
                <input placeholder="Password" />
            </div>
            <div class="row">
                <div class="col">
                    <a>Forgot password?</a>
                </div>
                <div class="col">
                    <p>Don't have an account yet? <a>Register now!</a></p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import NeosynBrand from '../components/NeosynBrand.vue';
</script>