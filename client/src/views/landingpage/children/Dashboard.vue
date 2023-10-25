<template>
    <div>
        <div class="row">
            <h1>Dashboard!</h1>
        </div>
        <div class="row">
            <template v-if="store.name != ''">
                <div>
                    <h4>Hallo, {{ store.name }}</h4>
                </div>
            </template>
            <div>
                <button @click="fbLogin">Login</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';
import {useFBStore} from "../../../store/fb"

const store = useFBStore()

onMounted(() => {
    
})

function fbLogin() {
}
</script>

<style scoped>

</style>