<template>
  <div class="bg-darkgray basis-1/2 rounded-xl flex flex-col">
    <img width="410" height="410" src="/assets/stock/post.jpg" alt="">
    <div class="flex justify-around items-center text-white py-4">
      <div class="flex gap-1 items-center">
        <heart
       class="text-red-600"
        /> 800 Likes
      </div>
      <div class="flex gap-1 items-center">
        <comments/> 84 Comments
      </div>
      <div class="flex gap-1 items-center">
        <retweets/> Retweets
      </div>
    </div>
    <div class="px-4 py-2 text-white">
      <p>ARE YOU READY? 🤤Nur noch 7 TAGE und eure creamy dreams werden wahr 🫠Am Dienstag launchen wir exklusiv in unserem Onlineshop einen neuen nucao Schokoriegel! 💥So viel vorweg: Es wird extreeeeem cremig, nussig und sau lecker.Welche Riegelsorte wird es wohl werden? 👀Unter allen Antworten in den Kommentaren verlosen wir zweimal eine 12er Packung der neuen Sorte!Ratet bis zum 12.10.2023, 18 Uhr und probiert als erstes unseren neuen Riegel!
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

</template>
<script>

import Heart from '../global/heart.vue';
import Comments from '../global/comments.vue';
import Retweets from '../global/retweets.vue';
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
