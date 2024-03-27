<template>
  <section class="flex flex-row h-full">
    <sidebar-navigation/>
    <div class="overflow-y-scroll px-4 py-4">
      <router-view></router-view>
    </div>
  </section>
</template>
<script>

import ProgressBar from '../components/global/ProgressBar.vue';
import SidebarNavigation from '../components/navigation/SidebarNavigation.vue';

export default {
  name: 'Home',
  components: {SidebarNavigation, ProgressBar},
  data: () => {
    return {
      progress: 10,
      percentage: 100,
    }


  },
  computed: {},
  methods: {
    increaseProgress() {
      this.progress += 10;
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>