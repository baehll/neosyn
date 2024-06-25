<template>
  <div class="border border-lightgray-80 bg-darkgray h-1/2 overflow-hidden rounded-xl flex flex-col justify-between">
    <div
      v-if="messagePost"
      class="flex flex-col h-full"
    >
      <img class="shrink-0" width="410" height="410" :src="image">
      <div class="shrink-0 flex justify-around items-center text-white py-4 font-roboto font-medium text-sm">
        <div class="flex gap-1 items-center">
          <heart
          class="text-red-600"
        />
          <span v-text="getLikes"></span> <span class="hide-on-small" v-text="$t('Likes')"></span>
        </div>
        <div class="flex gap-1 items-center">
          <comments/>
          <span v-text="getComments"></span> <span class="hide-on-small" v-text="$t('Comments')"></span>
        </div>
        <div class="flex gap-1 items-center">
          <retweets/>
          <span v-text="getShares"></span> <span class="hide-on-small" v-text="$t('Retweets')"></span>
        </div>
      </div>
      <div class="overflow-y-scroll px-4 pt-2 mb-2 text-white grow-0">
        <p class="text-sm font-roboto font-medium" v-text="content"></p>
      </div>
    </div>
    <div
      class="relative h-full"
      v-else
    >
      <div class="absolute text-white top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2" v-text="$t('No message selected')">
      </div>
    </div>
  </div>

</template>
<script>

import Heart from '../global/heart.vue';
import Comments from '../global/comments.vue';
import Retweets from '../global/retweets.vue';
import ArrowUp from '../global/arrow-up.vue';

export default {
  name: 'MessagePost',
  components: {ArrowUp, Retweets, Comments, Heart},
  props: {
    messagePost: {
      type: Object
    },
    image: {
      type: String,
    },
    content: {
      type: String,
    },
    likes: {
      type: Number
    },
    comments: {
      type: Number
    },
    shares: {
      type: Number,
      default: 0
    }
  },
  data: () => {
    return {}
  },
  computed: {
    getShares(){
      return this.shares || 0
    },
    getComments(){
      return this.comments || 0
    },
    getLikes(){
      return this.likes || 0
    }
  },
  methods: {},
  created: () => {

  }
}
</script>

<style lang="scss">
.hide-on-small {
  @apply hidden;

  @media (min-width: 1650px){
    @apply inline-block;
  }
}
</style>
