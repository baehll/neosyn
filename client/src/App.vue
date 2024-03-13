<template>
  <transition name="fade">
    <router-view></router-view>
  </transition>
</template>
<script>
export default {
  name: "App",
  components: {
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
