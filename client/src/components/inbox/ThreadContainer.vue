<template>
  <div class="bg-darkgray shrink-0 thread-container flex flex-col">
    <ThreadTopBar
      @triggeredSearch="updateSearchTermAndFetch"
      @changedFilter="updateFilterAndFetch"
      @changeSorting="updateSortingAndFetch"
    />
    <div class="scroller overflow-y-scroll">
      <Thread
        v-for="thread in threadStore.threads"
        :key="thread.id"
        :id="thread.id"
        :is-selected="selectedThreadId === thread.id"
        :username="thread.username"
        :message="thread.message"
        :last-updated="thread.lastUpdated"
        :platform="thread.platform"
        :unread="thread.unread"
        @selected="setSelectedThread"
        @toggle-unread="toggleUnreadStatus"
        @delete="deleteThread"
      />
    </div>
  </div>
</template>
<script>

import {mapStores} from 'pinia';
import {useThreadStore} from '../../stores/thread.js';
import ThreadTopBar from './ThreadTopBar.vue';
import Thread from './Thread.vue';
import ThreadService from '../../services/ThreadService.js';

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
    async toggleUnreadStatus(id) {
      const thread = this.threadStore.threads.find(t => t.id === id)
      try{
        await ThreadService.toggleUnreadStatus(id, !thread.unread)
        this.threadStore.threads.find(t => t.id === id).unread = !thread.unread
      } catch (e){

      }
    },
    async deleteThread(id){
      try{
        await ThreadService.deleteThread(id)
      } catch (e){
      }
      this.threadStore.threads = this.threadStore.threads.filter(t => t.id !== id) 
    },
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
    await this.fetchThreads()
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
  width: 292px;

  @media (min-width: 1920px){
    width: 370px;
  }
}
.scroller {
  scrollbar-color: #212121 #3e3e3e;
}
</style>
