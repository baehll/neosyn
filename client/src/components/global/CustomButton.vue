<template>
  <component :is="tag" class="" :disabled="disabled">
    <slot></slot>
  </component>
</template>
<script>

export default {
  props: {
    tag: {
      type: String,
      default: 'button'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  name: 'CustomButton',
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
button, a {
  @apply px-4 py-2.5 transition-all;
  border-radius: 10px;

  &.primary {
    @apply bg-primary text-darkgray;
  }

  &.outlined {
    @apply border border-lightgray-60 bg-transparent text-lightgray-60;
  }

  &.icon-only {
    @apply bg-transparent text-lightgray-10 px-0 py-0;
  }

  &.ghost {
    @apply bg-transparent text-lightgray-10;
  }
}

button[disabled] {
  @apply bg-lightgray-60;
}

</style>