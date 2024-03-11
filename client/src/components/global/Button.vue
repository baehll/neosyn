<template>
  <button v-text="cta">
  </button>

</template>
<script>

export default {
  props: {
    cta: {
      type: String,
      default: ''
    }
  },
  name: 'Button',
  data: () => {
    return {}
  },
  computed: {},
  methods: {},
  created: () => {

  }
}
</script>

<style lang="scss">

</style>