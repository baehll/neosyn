<template>
  <ThreadContainer
    @selected-thread="setSelectedThread"
  />
  <MessageContainer
    :thread-id="currentThreadId"
  />
  <PostContainer
    v-if="minScreenWidth"
    :thread-id="currentThreadId"
  />
</template>
<script>

import ThreadContainer from '../components/inbox/ThreadContainer.vue';
import MessageContainer from '../components/inbox/MessageContainer.vue';
import {mapStores} from 'pinia';
import {useThreadStore} from '../stores/thread.js';
import PostContainer from '../components/inbox/PostContainer.vue';

export default {
  name: 'InboxView',
  components: {
    PostContainer,
    MessageContainer,
    ThreadContainer
  },
  data: () => {
    return {
      currentThreadId: null,
    }
  },
  computed: {
    ...mapStores(useThreadStore),
    minScreenWidth(){
      return window.innerWidth > 1400
    }
  },
  methods: {
    setSelectedThread(id) {
      this.currentThreadId = id
      this.threadStore.markThreadAsRead(id)
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
</style>
