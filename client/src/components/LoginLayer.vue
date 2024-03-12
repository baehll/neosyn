<template>
  <div
    :class="{'transition-opacity backdrop-blur-xl bg-darkgray/40 h-full w-full': true, 'opacity-0 pointer-events-none': !loginVisible, 'opacity-100 pointer-events-all': loginVisible}">
    <div
      class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2 px-8 py-3 w-64 bg-darkgray/40 rounded-lg border border-lightgray">
      <strong class="text-white text-center uppercase block mb-6 font-neuebit text-xl">
        Early Access
      </strong>
      <input type="text" placeholder="Password" v-model="password" @keyup.enter="login">
      <close/>
    </div>
  </div>
</template>
<script>

import Close from './global/close.vue';
import EarlyAccess from '../services/EarlyAccess.js';

export default {
  name: 'LoginLayer',
  components: {Close},
  emits: [
    'hide'
  ],
  props: {
    loginVisible: {
      type: Boolean,
      default: false,
    }
  },
  data: () => {
    return {
      password: ''
    }
  },
  computed: {},
  methods: {
    async login() {
      const {data} = await EarlyAccess.login(this.password)
      console.log(data);
    }
  },
  mounted: function () {
    window.addEventListener('keydown', e => {
      if (!this.loginVisible) {
        return
      }
      if (e.key === 'Escape') {
        this.password = ''
        this.$emit('hide')
      }
    });
  },
  created: function () {

  }
}
</script>

<style lang="scss" scoped>
input {
  @apply bg-lightgray rounded-lg px-6 py-3 text-lightgray-10 text-sm;
}
</style>