<template>
  <button class="" :disabled="disabled">
    <slot></slot>
  </button>
</template>
<script>

export default {
  props: {
    disabled: {
      type: Boolean,
      default: false
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

<style lang="scss" scoped>
button {
  @apply bg-primary text-darkgray px-4 py-2 rounded transition-all;

  &.icon-only {
    @apply bg-transparent text-lightgray-10 px-0 py-0;
  }

  &.ghost {
    @apply bg-transparent text-lightgray-10;
  }

  &[disabled] {
    @apply bg-lightgray-60;
  }
}

</style>