<template>
  <div class="grow overflow-hidden h-full px-5 py-5 bg-lightgray">
    <div class="overflow-hidden flex flex-col justify-between w-full h-full bg-darkgray rounded-xl message p-4">
      <div class="flex justify-between p-6">
        <span class="rounded-3xl border border-white px-4 text-white py-1" v-text="$t('Interaction')"></span>
        <BookmarkOutline
          class="text-darkgray-80"
        />
      </div>
      <div class="messages flex-grow relative">
        <div class="pl-2 pr-5 pt-4 pb-6 messages items-start flex flex-col h-full overflow-scroll absolute top-0 left-0 " ref="messageScroller">
          <!--CustomButton
            :cta="$t('Mehr laden')"
            v-if="hasMoreMessages"
            @click="loadMoreMessages"
            :loading="loadMessageLoading"
            type="x-btn--primary"
            class-name="flex-shrink-0"
          /-->
          <Message
            v-for="message in messageStore.messages[1]"
            :message="message.message"
            :from="message.from"
            :id="message.id"
            :date="message.date"
          />
        </div>
      </div>
      <div class="actions shrink-0">
        <div class="quick-responses"></div>
        <div class="generate-responses p-4 border border-lightgray rounded-xl flex justify-between">
          <CustomButton
            class="font-medium font-roboto text-sm bg-primary flex flex-row items-center gap-3 rounded-2xl"
          >
            {{ $t('Generate') }}
            <stars
              class="text-black"
            />
          </CustomButton>
          <button class="bg-lightgray">
            <arrow-up
              class="text-black"
            />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import BookmarkOutline from '../global/bookmark-outline.vue';
import CustomButton from '../global/CustomButton.vue';
import Stars from '../global/stars.vue';
import ArrowUp from '../global/arrow-up.vue';
import Message from './Message.vue';
import {mapStores} from 'pinia';
import {useMessageStore} from '../../stores/message.js';
import {useThreadStore} from '../../stores/thread.js';

export default {
  name: 'MessageContainer',
  components: {Message, ArrowUp, Stars, CustomButton, BookmarkOutline},
  props: {
    threadId: {
      type: Number,
    }
  },
  data: () => {
    return {
      msg: 'Not watching message',
    }
  },
  watch: {
    threadId(oldVal, newVal) {
      this.messageStore.getMessagesForThread(newVal)
      setTimeout(() => {
        this.$refs.messageScroller.scrollTo({top: this.$refs.messageScroller.scrollHeight, behavior: 'smooth'})
      }, 250)
    }
  },
  computed: {
    ...mapStores(useThreadStore, useMessageStore)
  },
  methods: {},
  created: () => {

  }
}
</script>

<style lang="scss">

</style>