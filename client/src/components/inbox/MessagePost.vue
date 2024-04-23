<template>
  <div class="bg-darkgray h-1/2 overflow-hidden rounded-xl flex flex-col justify-between">
    <div class="flex flex-col h-full">
      <img class="shrink-0" width="410" height="410" src="/assets/stock/post.jpg" alt="">
      <div class="shrink-0 flex justify-around items-center text-white py-4 font-roboto font-medium text-sm">
        <div class="flex gap-1 items-center">
          <heart
            class="text-red-600"
          />
          800 <span class="hide-on-small">Likes</span>
        </div>
        <div class="flex gap-1 items-center">
          <comments/>
          84 <span class="hide-on-small">Comments</span>
        </div>
        <div class="flex gap-1 items-center">
          <retweets/>
          11 <span class="hide-on-small">Retweets</span>
        </div>
      </div>
      <div class="px-4 py-2 text-white grow-0">
        <p class="text-sm font-roboto font-medium">ARE YOU READY? 🤤Nur noch 7 TAGE und eure creamy dreams werden wahr 🫠Am Dienstag launchen wir exklusiv in
          unserem Onlineshop einen neuen nucao Schokoriegel! 💥So viel vorweg: Es wird extreeeeem cremig, nussig und sau
          lecker.Welche Riegelsorte wird es wohl werden? 👀Unter allen Antworten in den Kommentaren verlosen wir zweimal
          eine 12er Packung der neuen Sorte!Ratet bis zum 12.10.2023, 18 Uhr und probiert als erstes unseren neuen Riegel!
          .
          .
          .
          .
          .
          .
          .
          .
          .
          .
          #Lorem #Ipsum #Dolor
        </p>
      </div>
    </div>
    <div class="h-8 shrink-0 bg-darkgray-80 grow flex justify-center items-center">
      <arrow-up
        class="transform rotate-180 text-lightgray"
      />
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
  data: () => {
    return {}
  },
  computed: {},
  methods: {},
  created: () => {

  }
}
</script>

<style lang="scss">
.enlarge {
}
</style>
