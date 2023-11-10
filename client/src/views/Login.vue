<template>
    <div class="row">
        <NeosynBrand></NeosynBrand>
    </div>
    <div class="row">
        <div class="col">
            <h4>Login</h4>
            <form class="row">
                <input placeholder="Username" :ref="username"/>
                <input placeholder="Password" :ref="pw"/>
                <button class="btn btn-primary" >Submit</button>
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