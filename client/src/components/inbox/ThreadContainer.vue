<template>
  <div class="bg-darkgray-10 shrink-0 thread-container flex flex-col">
    <ThreadTopBar
      @triggeredSearch="updateSearchTermAndFetch"
      @changedFilter="updateFilterAndFetch"
      @changeSorting="updateSortingAndFetch"
    />
    <div class="overflow-y-scroll py-4">
      <Thread
        v-for="thread in threadStore.threads"
        :key="thread.id"
        :id="thread.id"
        :is-selected="selectedThreadId === thread.id"
        :username="thread.username"
        :message="thread.last_message"
        :lastUpdated="thread.last_updated"
        :platform="thread.platform"
        :unread="thread.unread"
        @selected="setSelectedThread"
      />
    </div>
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
import ThreadTopBar from './ThreadTopBar.vue';
import Thread from './Thread.vue';

export default {
  name: 'ThreadContainer',
  components: {Thread, ThreadTopBar},
  emits:['selectedThread'],
  data: () => {
    return {
      selectedThreadId: null,
      filters: [],
      searchTerm: '',
      sorting: 'asc',
    }
  },
  computed: {
    ...mapStores(useThreadStore)
  },
  methods: {
    async fetchThreads() {
      this.threadStore.fetchThreads()
    },

    async updateSortingAndFetch() {
      return this.fetchThreads()
    },
    async updateFilterAndFetch() {
      return this.fetchThreads()
    },
    async updateSearchTermAndFetch() {
      return this.fetchThreads()
    },
    async setSelectedThread(id) {
      this.selectedThreadId = id
      this.$emit('selectedThread', id)
    }
  },
  async created() {
    this.fetchThreads()
  }
}
</script>

<style lang="scss">
.thread {
  &.selected {
    @apply bg-lightgray;
  }
}
.thread-container {
  width: 370px;
}
</style>
