<template>
  <div class="bg-darkgray shrink-0 border-r border-r-lightgray-80 thread-container flex flex-col">
    <ThreadTopBar
      @triggeredSearch="updateSearchTermAndFetch"
      @changedFilter="updateFilterAndFetch"
      @changedSorting="updateSortingAndFetch"
      @reload="fetchThreads"
    />
    <div class="scroller overflow-y-scroll">
      <div class="thread-loader" v-if="threadsLoading">
        <div></div>
        <div></div>
        <div></div>
      </div>
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
      threadsLoading: false,
      selectedThreadId: null,
      filters: [],
      searchTerm: null,
      sorting: null,
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
      this.threadsLoading = true
      await this.threadStore.fetchThreads(this.filters, this.searchTerm, this.sorting)
      this.threadsLoading = false
    },
    async updateSortingAndFetch(sorting) {
      this.sorting = sorting
      return this.fetchThreads()
    },
    async updateFilterAndFetch(filters) {
      this.filters = filters
      return this.fetchThreads()
    },
    async updateSearchTermAndFetch(searchTerm) {
      this.searchTerm = searchTerm
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

<style lang="scss" scoped>
@keyframes loader {
  0% {
    transform: translate3d(-50%,0,0);
  }
  25% {
    transform: translate3d(-100%,0,0);
  }
50% {
    transform: translate3d(-50%,0,0);
}
  75% {
    transform: translate3d(-0%,0,0);
  }
100% {
    transform: translate3d(-50%,0,0);
}
}
.thread-loader {
  > div {
    @apply rounded-xl mb-4 relative overflow-hidden mx-auto;
    width: 85%;
    height: 90px;
    &:before {
      content: '';
      position: absolute;
      left: 50%;
      top: 0;
      width: 120%;
      height: 100%;
      transform: translate3d(-50%,0,0);
      background: rgb(0,0,0);
      background: linear-gradient(90deg, rgba(44,44,44,0) 0%, #6f6f6f 50%, rgba(44,44,44,0) 100%);
      animation: loader 1.7s linear infinite;
    }
  }
}
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
