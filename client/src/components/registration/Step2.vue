<template>
  <div>
    <h2 v-text="$t('What is your company\'s name?')"></h2>
    <p class="mb-3">Lorem ipsum dolor sit amet.</p>
    <input ref="input" @keyup.enter="$emit('nextStep')" @keyup="type" type="text" v-model="company" autofocus
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
  name: 'Registration Step 2',
  components: {IdCard, Button},
  data: () => {
    return {
      company: ''
    }
  },
  computed: {
    ...mapStores(useUserStore)
  },
  methods: {
    nextStep() {
      this.$emit('nextStep')
    },
    type() {
      this.userStore.company = this.company
    }
  },
  mounted() {
    this.$refs.input.focus()
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>
