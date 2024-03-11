<template>
<div class="bg-lightgray-10 rounded-lg p-4 w-1/5">
  <div class="bg-darkgray rounded-lg h-72 flex items-end justify-center">
    <user/>
  </div>
  <div class="flex justify-between flex-col">
    <div>
      <h3 v-text="name"></h3>
      <h5 v-text="company"></h5>

    </div>
    <small>Registered 23.04.2024</small>
  </div>

</div>
</template>
<script>
import {mapStores} from 'pinia';
import {useUserStore} from '../stores/user.js';
import User from './global/user.vue';

export default {
  name: "IdCard",
  components: {User},
  computed: {
    ...mapStores(useUserStore),
    name(){
      return this.userStore.name
    },
    company(){
      return this.userStore.company
    },
    image(){
      return this.userstore.image
    }
  }
}
</script>
<style scoped>

</style>