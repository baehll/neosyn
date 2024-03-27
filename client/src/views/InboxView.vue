<template>
  <Inbox
    @selectedThread="selectedThread"
  />
 <div class="w-full h-full px-6 py-6 bg-lightgray">

 </div>
</template>
<script>

import Inbox from '../components/inbox/Inbox.vue';

export default {
  name: 'InboxView',
  components: {Inbox},
  data: () => {
    return {}
  },
  computed: {},
  methods: {
    selectedThread() {
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>