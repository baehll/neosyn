<template>
  <div
    :class="{'transition-opacity backdrop-blur-xl bg-darkgray/40 h-full w-full': true, 'opacity-0 pointer-events-none': !loginVisible, 'opacity-100 pointer-events-all': loginVisible}">
    <div
      class="absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2 px-16 py-12 bg-darkgray/40 rounded-lg border border-lightgray wrapper">
      <strong class="text-white text-center uppercase block mb-6 font-neuebit text-xl">
        Early Access
      </strong>
      <input type="text" placeholder="Password" v-model="password" @keyup.enter="login" class="w-full block">
      <button class="absolute top-4 right-4" @click="$emit('hide')">
        <close class="text-lightgray-10" />
      </button>
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
      const response = await EarlyAccess.login(this.password)
      if (response.status === 200) {
        this.$router.push('/login')
      }
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
.wrapper {
  width: 680px;
}
input {
  @apply bg-lightgray rounded-lg px-6 py-3 text-lightgray-10 text-sm;
}
</style>