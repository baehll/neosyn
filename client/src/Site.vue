<template>
  <transition name="fade">
    <router-view></router-view>
  </transition>
</template>
<script>

export default {
  name: "Site",
}
</script>

<style lang="scss">
html{
  #app {
    height: 100vh;
  }

  @media (min-width: 1024px) and (max-width: 1730px) {
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


</style>
