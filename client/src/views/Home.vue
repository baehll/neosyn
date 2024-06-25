<template>
  <section class="pr-5 bg-lightgray-30 flex flex-row h-full">
    <sidebar-navigation/>
    <router-view></router-view>
  </section>
</template>
<script>

import SidebarNavigation from '../components/navigation/SidebarNavigation.vue';

export default {
  name: 'Home',
  components: {SidebarNavigation},
  data: () => {
    return {
    }
  },
  computed: {},
  methods: {
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>
