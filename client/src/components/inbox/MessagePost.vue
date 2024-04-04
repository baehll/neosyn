<template>
  <div class="rounded-xl flex flex-col">
    <img src="" alt="">
    <div class="flex justify-center items-center">
      <div class="flex gap-1">
        <heart/> 800 Likes
      </div>
      <div class="flex gap-1">
        <comments/> 84 Comments
      </div>
      <div class="flex gap-1">
        <retweets/> Retweets
      </div>
    </div>
  </div>

</template>
<script>

import Heart from '../global/heart.vue';
import Comments from '../global/comments.vue';
import Retweets from '../global/retweets.vue';
// unaite
export default {
  name: 'MessagePost',
  components: {Retweets, Comments, Heart},
  data: () => {
    return {

    }
  },
  computed: {

  },
  methods: {

  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>
