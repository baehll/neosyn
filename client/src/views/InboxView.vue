<template>
  <ThreadContainer
    @selected-thread="setSelectedThread"
  />
  <MessageContainer
    :thread-id="currentThread"
  />
  <div class=" message-post-wrap  h-full py-5 bg-lightgray pr-5">
    <div class="overflow-hidden flex flex-col justify-between w-full h-full bg-darkgray rounded-xl message ">
      <MessagePost

      />
      <MessageInsights

      />
    </div>
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
.message-post-wrap {
  width: 410px;
}
</style>