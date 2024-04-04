<template>
  <ThreadContainer
    @selected-thread="setSelectedThread"
  />
  <MessageContainer
    :thread-id="currentThread"
  />
  <div class="flex flex-col h-full">
    <MessagePost

     />
    <MessageInsights

      />
  </div>
</template>
<script>

import Inbox from '../components/inbox/Inbox.vue';
import Message from '../components/inbox/MessageContainer.vue';
import ThreadContainer from '../components/inbox/ThreadContainer.vue';
import MessageContainer from '../components/inbox/MessageContainer.vue';
import {mapStores} from 'pinia';
import {useThreadStore} from '../stores/thread.js';
import MessagePost from '../components/inbox/MessagePost.vue';
import MessageInsights from '../components/inbox/MessageInsights.vue';

export default {
  name: 'InboxView',
  components: {MessageInsights, MessagePost, MessageContainer, ThreadContainer, Message, Inbox},
  data: () => {
    return {
      currentThread: null,

    }
  },
  computed: {
    ...mapStores(useThreadStore)
  },
  methods: {
    setSelectedThread(id) {
      this.currentThread = id
      this.threadStore.markThreadAsRead(id)
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>