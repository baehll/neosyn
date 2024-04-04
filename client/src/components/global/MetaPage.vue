<template>
  <div class="pt-8 px-8 md:pt-20 lg:px-20 lg:pb-16 h-full relative flex flex-col">
    <div class="flex flex-col lg:items-center justify-between lg:flex-row">
      <h1 v-text="title" class="font-neuebit text-4xl lg:text-7xl text-primary flex-basis-full"></h1>
      <ul class="flex flex-row gap-6 text-lightgray-10">
        <slot name="navigation"></slot>
      </ul>
    </div>
    <div class="content mt-8 lg:mt-16 h-full overflow-y-scroll ">
      <div class="flex lg:flex-row flex-col text-white lg:px-12 lg:items-end">
        <slot name="content"></slot>
      </div>
    </div>
    <logo-big class="footer absolute right-8 bottom-8 lg:right-20 md:bottom-16 text-primary"/>
  </div>
</template>
<script>

import Logo from './logo.vue';
import LogoBig from './logo-big.vue';

export default {
  name: 'MetaPage',
  components: {LogoBig, Logo},
  emits: [],
  props: {
    title: {
      type: String,
      default: ''
    }
  },
  data: () => {
    return {}
  },
  computed: {},
  methods: {},
  mounted: function () {

  },
  created: function () {

  }
}
</script>

<style lang="scss" scoped>

</style>
