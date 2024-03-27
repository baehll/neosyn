<template>
  <transition name="fade">
    <Home/>
  </transition>
</template>
<script>
import Home from './views/Home.vue';
import {mapStores} from 'pinia';
import {useTimerStore} from './stores/timer.js';

export default {
  name: "App",
  components: {
    Home
  },
  computed: {
    ...mapStores(useTimerStore)
  },
  created(){
    setInterval(() => {
      this.timerStore.now = Date.now()
    }, 60 * 1000)
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}


</style>
