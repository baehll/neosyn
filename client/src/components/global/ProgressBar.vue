<template>
  <div class="rounded-md bg-lightgray h-2 relative overflow-hidden">
    <div :style="{transform: `translate3d(-${100 - percentage}%, 0, 0)`}" class="transition-transform bg-primary absolute left-0 h-full w-full"></div>
  </div>
</template>
<script>

export default {
  name: 'ProgressBar',
  props: {
    percentage: {
      type: Number,
      default: 0
    }
  },
  data: () => {
    return {

    }
  },
  computed: {

  },
  methods: {

  },
  created: function(){

  }
}
</script>

<style lang="scss">

</style>