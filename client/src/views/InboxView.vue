<template>
  <ThreadContainer
@selected-thread="setSelectedThread"
  />
  <MessageContainer
:thread-id="currentThread"
  />
</template>
<script>

import Inbox from '../components/inbox/Inbox.vue';
import Message from '../components/inbox/MessageContainer.vue';
import ThreadContainer from '../components/inbox/ThreadContainer.vue';
import MessageContainer from '../components/inbox/MessageContainer.vue';

export default {
  name: 'InboxView',
  components: {MessageContainer, ThreadContainer, Message, Inbox},
  data: () => {
    return {
      currentThread: null,

    }
  },
  computed: {},
  methods: {
    setSelectedThread(id) {
      this.currentThread = id
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>