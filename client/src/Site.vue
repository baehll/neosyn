<template>
  <transition name="fade">
    <router-view></router-view>
  </transition>
</template>
<script>
import ComingSoon from './views/ComingSoon.vue';

export default {
  name: "Site",
  components: {
    ComingSoon
  },
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
