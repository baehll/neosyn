<template>
  <div>
    <h2 v-text="$t('What is your name?')"></h2>
    <p class="mb-3">Lorem ipsum dolor sit amet.</p>
    <input @keyup="type" type="text" v-model="name" @keyup.enter="$emit('nextStep')" autofocus
           class="border border-lightgray rounded-lg w-full bg-transparent">
  </div>
</template>
<script>

import Button from '../global/Button.vue';
import IdCard from '../IdCard.vue';
import {mapStores} from 'pinia';
import {useUserStore} from '../../stores/user.js';

export default {
  emits: ['nextStep'],
  name: 'Registration Step 1',
  components: {IdCard, Button},
  data: () => {
    return {
      name: ''
    }
  },
  computed: {
    ...mapStores(useUserStore),
  },
  methods: {
    nextStep() {
      this.$emit('nextStep')
    },
    type() {
      this.userStore.name = this.name
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>