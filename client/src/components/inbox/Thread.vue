<template>
  <div
    :class="'cursor-pointer transition-colors hover:bg-lightgray-20 text-white thread py-4 px-5 border-b border-lightgray relative ' + getInteractiveClasses"
    @click="selectThread"
  >
    <span
      class="absolute left-2 top-6 rounded-full bg-primary w-2 h-2"
      v-if="unread === true"
    >

    </span>
    <strong v-text="username" class="font-roboto block mb-3"></strong>
    <p class="roboto font-light text-sm mb-3" v-text="message"></p>
    <div
      @mouseenter="showThreadActions"
      @mouseleave="hideThreadActions"
      class="absolute top-4 right-3 leading-none w-32 h-4"
    >
      <TimeDifferenceDisplay
        class=""
        :class="{'text-lightgray-10 text-xs absolute right-0': true, 'opacity-0 pointer-events-none': threadActionVisible}"
        :point-in-time="lastUpdated"
      />
      <div
        class=""
        :class="{'items-center justify-end flex flex-row gap-4 absolute right-0': true, 'opacity-0 pointer-events-none': !threadActionVisible}"
      >
        <button
          @click.stop="toggleUnreadStatus"
        >
          <EnvelopeOpen
            class="hover:text-primary text-darkgray-80"
          />
        </button>
        <button
          @click="deleteMessage"
        >
          <Trash
            class="hover:text-primary text-darkgray-80"
          />
        </button>
      </div>
    </div>

    <IconResolver
      :class="{'text-lightgray-10 absolute right-3 bottom-4 transition-all opacity-100': true, }"
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
import EnvelopeOpen from '../global/envelope-open.vue';
import Trash from '../global/trash.vue';

export default {
  name: 'Thread',
  components: {Trash, EnvelopeOpen, TimeDifferenceDisplay, IconResolver},
  emits: ['selected'],
  props: {
    id: {
      type: Number,
    },
    unread: {
     type: Boolean,
     default: true
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
    return {
      threadActionVisible: false,
    }
  },
  computed: {
    getInteractiveClasses() {
      return this.isSelected ?
        'bg-lightgray' :
        'bg-transparent'
    },
    ...mapStores(useThreadStore, useTimerStore),
  },
  methods: {
    toggleUnreadStatus(e){
      this.$emit('toggle-unread', this.id)
    },
    deleteMessage(){
      this.$emit('delete', this.id)
    },
    showThreadActions() {
      this.threadActionVisible = true
    },
    hideThreadActions() {
      this.threadActionVisible = false
    },
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
  &:first-child {
    @apply border-t;
  }

  &.selected {
    @apply bg-lightgray;
  }
}
</style>
