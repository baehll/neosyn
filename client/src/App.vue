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
import {useUserStore} from './stores/user.js';
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
      app: document.getElementById('app'),
    }
  },
  computed: {
    ...mapStores(useTimerStore, useUserStore)
  },
  methods: {
    checkResolution() {
      const innerWidth = window.innerWidth;
      const innerHeight = window.innerHeight;
      this.resolutionTooLow = false // innerWidth <= 1600 || innerHeight <= 1150
    }
  },
  async created() {
    this.userStore.me()
    addEventListener('resize', this.checkResolution);
    this.checkResolution();

    setInterval(() => {
      this.timerStore.now = Date.now()
    }, 20*1000)
  }
}
</script>

<style lang="scss">
html{
  #app {
    height: 100vh;
  }

  @media (max-width: 1730px) {
    -moz-transform: scale(0.8, 0.8);
    -ms-transform: scale(0.8);
    -webkit-transform: scale(0.8);
    transform: scale(0.8);

    width:125%; /* to compensate for the 0.8 scale */
    transform-origin:0 0; /* to move it back to the top left of the window */
    #app {
      height: 125vh;
    }
  }
}
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
