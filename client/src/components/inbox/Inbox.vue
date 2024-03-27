<template>
  <ThreadTopBar
    @triggeredSearch="updateSearchTermAndFetch"
    @changedFilter="updateFilterAndFetch"
    @changeSorting="updateSortingAndFetch"
  />
  <Thread
    v-for="thread in threadStore.threads"
    :key="thread.id"
    :username="thread.username"
    :message="thread.last_message"
    :lastUpdated="thread.last_updated"
    :platform="thread.platform"
    @selected="fetchMessage"
  />
</template>
<script>

import ThreadTopBar from './ThreadTopBar.vue';
import Thread from './Thread.vue';
import {mapStores} from 'pinia';
import {useThreadStore} from '../../stores/thread.js';

export default {
  name: 'Inbox',
  components: {Thread, ThreadTopBar},
  data: () => {
    return {
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
    async fetchMessage() {
    }
  },
  async created (){
    this.fetchThreads()
  }
}
</script>

<style lang="scss">

</style>