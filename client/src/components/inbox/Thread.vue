<template>
  <div class="text-lightgray-10 thread py-4 px-3 border-b border-lightgray" @click="$emit('selected', id)">
    <strong v-text="username" class="font-roboto block mb-2"></strong>
    <p class="roboto font-light" v-text="message"></p>
    <TimeDifferenceDisplay
      class="text-lightgray-10"
      :point-in-time="lastUpdated"
    />
    <IconResolver
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
  },
  data: () => {
    return {}
  },
  computed: {
    ...mapStores(useThreadStore, useTimerStore),
  },
  methods: {},
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