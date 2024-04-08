<template>
    <component :is="tag" :disabled="disabled"
      :class="{'font-medium font-roboto text-sm flex flex-row items-center gap-3 rounded-2xl grow-0': true, 'cursor-pointer': !disabled}"
  >
    <span>
      <p>
        <slot></slot>
      </p>
      <Stars
      />
    </span>
  </component>
</template>
<script>
import Stars from './stars.vue';


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
  name: 'GenerateButton',
  data: () => {
    return {}
  },
  computed: {},
  components:{
    Stars
  },
  methods: {},
  created: () => {

  }
}
</script>

<style lang="scss" scoped>
@keyframes rotate-gradient {
0% {
  transform: rotate(0deg) translate(-50%, -50%);
}
100% {
  transform: rotate(360deg) translate(-50%, -50%);
}
}
button, a {
  &:before {
    content: '';
    @apply absolute transform -translate-x-1/2 -translate-y-1/2 left-1/2 top-1/2 w-full flex;
    width: calc(100% + 4px);
    transform-origin: -0% -0%;
    border-radius: 10px;
      aspect-ratio: 1/1;
      // background-image: radial-gradient(circle,  #ACED84 0%, #D9FFC1 50%)
       background-image: linear-gradient(0deg, #ACED84 0%,#ACED84 45%, #D9FFC1 50%)
  }

  &:hover {
    &:before {
    animation: rotate-gradient 2s linear infinite; 
    }

    span {
      @apply bg-lightgray-20;
    }
  }

  @apply shrink-0 overflow-hidden relative transition-all text-sm ;
  padding: 1px;
  border-radius: 10px;

  span {
    @apply gap-2 transition-colors text-primary py-2.5 px-4 z-10 bg-darkgray flex;
    border-radius: 10px;
    p{
      @apply bg-gradient-to-t from-primary to-primary-10 inline-block text-transparent bg-clip-text;
    }
  }

  svg {
    @apply text-primary;
  }
}

button[disabled] {
  &:before {
    @apply hidden;
  }
  @apply bg-darkgray-80 text-black;
  svg, span {
    @apply text-black;
  }
}

</style>
