<template>
  <transition name="fade">
    <Home/>
  </transition>
  <ResolutionNotice v-if="resolutionTooLow"/>
</template>
<script>
import Home from './views/Home.vue';
import {mapStores} from 'pinia';
import {useTimerStore} from './stores/timer.js';
import ResolutionNotice from './components/global/ResolutionNotice.vue';

export default {
  name: "App",
  components: {
    ResolutionNotice,
    Home
  },
  data: () => {
    return {
      resolutionTooLow: false,
    }
  },
  computed: {
    ...mapStores(useTimerStore)
  },
  methods: {
    checkResolution() {
      const innerWidth = window.innerWidth;
      const innerHeight = window.innerHeight;
      this.resolutionTooLow = innerWidth <= 1600 || innerHeight <= 1150
    }
  },
  created() {
    addEventListener('resize', this.checkResolution);
    this.checkResolution();
    setInterval(() => {
      this.timerStore.now = Date.now()
    }, 60 * 1000)
  }
}
</script>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

input {
  &[type="text"] {
    @apply bg-transparent rounded-lg px-6 py-3 text-lightgray-10 text-sm;
  }
}

</style>
