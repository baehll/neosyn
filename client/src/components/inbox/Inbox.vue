<template>
  <div class="flex flex-col">
  </div>
</template>
<script>

import ThreadTopBar from './ThreadTopBar.vue';
import Thread from './ThreadContainer.vue';
import {mapStores} from 'pinia';
import {useThreadStore} from '../../stores/thread.js';

export default {
  name: 'Inbox',
}
</script>

<style lang="scss">

</style>