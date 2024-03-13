<template>
<div class="bg-lightgray-60 rounded-lg p-4 w-2/5">
  <div class="mb-2 bg-darkgray rounded-lg h-64 flex items-end justify-center">
    <user
      class="text-lightgray-60"
    />
  </div>
  <div class="text-white flex justify-between flex-col">
    <div>
      <h2 class="text-4xl font-bold" v-text="name"></h2>
      <h5 class="text-sm mb-24" v-text="company"></h5>
    </div>
    <small class="text-xs">Registered 23.04.2024</small>
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
      return this.userStore.name.trim() !== '' ?
        this.userStore.name :
        'Name'
    },
    company(){
      return this.userStore.company.trim() !== '' ?
        this.userStore.company :
        'Company'
    },
    image(){
      return this.userstore.image
    }
  }
}
</script>
<style lang="scss" scoped>
:root {
  @apply text-white;
}
</style>