<template>
  <div :class="'cursor-pointer transition-colors hover:bg-lightgray-20 text-lightgray-10 thread py-4 px-3 border-b border-lightgray relative ' + getInteractiveClasses" @click="selectThread">
    <strong v-text="username" class="font-roboto block mb-2"></strong>
    <p class="roboto font-light mb-3" v-text="message"></p>
    <TimeDifferenceDisplay
      class="text-darkgray-80 absolute top-4 right-3 text-xs"
      :point-in-time="lastUpdated"
    />
    <IconResolver
      class="text-lightgray-10 absolute right-3 bottom-4"
      :icon-name="platform"
    />
  </div>
</template>
<script>

import {mapStores} from 'pinia';
import {useThreadStore} from '../../stores/thread.js';
import IconResolver from '../global/IconResolver.vue';
import {useTimerStore} from '../../stores/timer.js';
import TimeDifferenceDisplay from '../global/TimeDifferenceDisplay.vue';

export default {
  name: 'Thread',
  components: {TimeDifferenceDisplay, IconResolver},
  emits: ['selected'],
  props: {
    id:{
      type: Number,
    },
    username: {
      type: String,
    },
    lastUpdated: {
      type: String,
    },
    platform: {
      type: String,
    },
    message: {
      type: String,
    },
    isSelected: {
      type: Boolean,
      default: false
    },
  },
  data: () => {
    return {}
  },
  computed: {
    getInteractiveClasses(){
      return this.isSelected ?
        'bg-lightgray' :
        'bg-transparent'
    },
    ...mapStores(useThreadStore, useTimerStore),
  },
  methods: {
    selectThread() {
      this.$emit('selected', this.id)
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
.thread {
  &.selected {
    @apply bg-lightgray;
  }
}
</style>