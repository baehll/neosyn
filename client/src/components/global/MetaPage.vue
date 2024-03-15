<template>
  <div class="pt-20 px-20 pb-16 h-full relative flex flex-col">
    <div class="flex flex-row items-center justify-between">
      <h1 v-text="title" class="font-neuebit text-7xl text-primary"></h1>
      <ul class="flex flex-row gap-6 text-lightgray-10">
        <slot name="navigation"></slot>
      </ul>
    </div>
    <div class="content mt-16 h-full overflow-scroll">
      <slot name="content"></slot>
    </div>
    <logo class="footer absolute right-20 bottom-16 text-primary"/>
  </div>
</template>
<script>

import Logo from './logo.vue';

export default {
  name: 'MetaPage',
  components: {Logo},
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