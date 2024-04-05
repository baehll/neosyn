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
        <div
          class="pl-2 pr-5 pt-4 pb-6 messages items-start flex flex-col h-full overflow-scroll absolute top-0 left-0 "
          ref="messageScroller">
          <!--CustomButton
            :cta="$t('Mehr laden')"
            v-if="hasMoreMessages"
            @click="loadMoreMessages"
            :loading="loadMessageLoading"
            type="x-btn--primary"
            class-name="flex-shrink-0"
          /-->
          <Message
            class="mb-6"
            v-for="message in messageStore.messages[currentThreadId]"
            :message="message.message"
            :from="message.from"
            :id="message.id"
            :date="message.date"
            :state="message.state"
          />
        </div>
        <div :class="{'message-curtain absolute top-0 left-0 transition-all h-full w-full bg-black': true, 'opacity-0 pointer-events-none': suggestions.length === 0, 'opacity-60 pointer-events-all': suggestions.length}">

        </div>
        <div :class="{'suggestions absolute bottom-0 right-0 transform transition-transform': true, 'translate-x-100': suggestions.length === 0, 'translate-x-0': suggestions.length > 0}">
          <Message
            v-for="(suggestion, i) in suggestions"
            :class="{'mb-6': true}"
            :selectable="true"
            :message="suggestion.message"
            :from="0"
            :message-subline="`Suggestion ${i+1}`"
            :selected="i === selectedSuggestion"
            @select="suggestionSelected(i)"
          />
        </div>
      </div>
      <div class="actions max-w-full">
        <div class="flex justify-end gap-4 quick-responses mb-8">
          <CustomButton
            v-for="quickResponse in quickResponses"
            @click="insertResponse(quickResponse)"
            v-text="quickResponse"
          >
          </CustomButton>
        </div>
        <div
          class="grow-0 items-end generate-responses p-4 border border-lightgray rounded-xl flex justify-between gap-4">
          <CustomButton
            class="font-medium font-roboto text-sm bg-primary flex flex-row items-center gap-3 rounded-2xl grow-0"
            @click="generateSuggestions"
          >
            {{ $t('Generate') }}
            <stars
              class="text-black"
            />
          </CustomButton>
          <span contenteditable @keyup="messageUpdated" ref="msgInput"
                class="text-sm bg-transparent resize-none outline-0 grow-0 text-white block w-full "></span>
          <button
            :class="{'outline-0 rounded-xl px-5 py-3 bg-lightgray grow-0': true, 'cursor-not-allowed': messageInput === '', 'bg-primary cursor-pointer': messageInput !== ''}"
            @click="sendMessage"
          >
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
import SuggestService from '../../services/SuggestService.js';

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
      selectedSuggestion: null,
      currentThreadId: null,
      quickResponses: [
        'Thanks! 💚',
        'I agree!',
        'Love it! 💚',
        'Cool!'
      ],
      msg: 'Not watching message',
      messageInput: '',
      suggestions: [],
    }
  },
  watch: {
    threadId(newVal, oldVal) {
      this.messageStore.getMessagesForThread(newVal)
      this.suggestions = []
      this.currentThreadId = newVal
      this.messageInput = ''
      setTimeout(() => {
        this.$refs.messageScroller.scrollTo({top: this.$refs.messageScroller.scrollHeight, behavior: 'smooth'})
      }, 250)
    }
  },
  computed: {
    ...mapStores(useThreadStore, useMessageStore),
  },
  methods: {
    suggestionSelected(i) {
      this.selectedSuggestion = i
      this.insertResponse(this.suggestions[i].message)
    },
    async generateSuggestions() {
      this.suggestions = await SuggestService.generateSuggestions(this.threadId)
    },
    insertResponse(message) {
      this.messageInput = message
      this.$refs.msgInput.innerText = message
    },
    messageUpdated(e) {
      this.messageInput = e.target.innerText
    },
    async sendMessage() {
      if (this.messageInput === '') {
        return
      }
      const message = {
        state: 'sending',
        message: this.messageInput,
        from: 0,
        threadId: this.currentThreadId,
        date: Date.now(),
      }
      this.selectedSuggestion = null
      this.suggestions = []
      this.messageStore.messages[this.currentThreadId].push(message)
      setTimeout(() => {
        this.$refs.messageScroller.scrollTo({top: this.$refs.messageScroller.scrollHeight, behavior: 'smooth'})
        this.messageStore.sendMessage(message)
        this.messageInput = ''
        this.$refs.msgInput.innerText = ''
      }, 250)
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
.quick-responses {
  button {
    @apply bg-lightgray text-lightgray-10;
  }
}
</style>