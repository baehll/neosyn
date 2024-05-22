<template>
  <div class="message-container grow overflow-hidden h-full px-5 py-5 bg-lightgray">
    <div class="overflow-hidden flex flex-col justify-between w-full h-full bg-darkgray rounded-xl message p-4">
      <div class="flex justify-between px-2 pt-2 pb-4">
        <span class="rounded-3xl border border-white px-4 text-white py-1" v-text="$t('Interaction')"></span>
        <button
          :class="{'bookmark-button': true, 'bookmarked': currentThread && currentThread.bookmarked}"
          @click="bookmarkThread"
        >
          <BookmarkOutline
            class="bookmark-icon custom-fill"
          />
        </button>
      </div>
      <div class="messages flex-grow relative">
        <div
          class="w-full pl-2 pr-5 pt-4 pb-6 messages items-start flex flex-col h-full overflow-scroll absolute top-0 left-0 "
          ref="messageScroller">
          <Message
          class="mb-6"
          v-for="message in messageStore.messages[currentThreadId]"
          :message="message.message"
          :from="message.from"
          :id="message.id"
          :date="message.messageDate"
          :state="message.state"
        />
        </div>
        <div
          :class="{'h-full flex-col grow shrink-0 justify-end items-end suggestions absolute bottom-0 right-0 transform transition-transform': true, 'translate-x-100': suggestions.length === 0, 'translate-x-0': suggestions.length > 0}"
        >
        <div
          @click="closeSuggestions"
          :class="{'message-curtain absolute top-0 left-0 transition-all h-full w-full bg-black': true, 'opacity-0 pointer-events-none': suggestions.length === 0, 'opacity-60 pointer-events-all': suggestions.length}"
        >

        </div>
          <div class="overflow-y-scroll h-full w-full pr-6">
            <MessageBody
              v-for="(suggestion, i) in suggestions"
              :class="{'relative mb-6 mr-6 left-full w-6/12 transform -translate-x-full': true}"
              :selectable="true"
              :message="suggestion"
              :from="0"
              :message-subline="`Suggestion ${i+1}`"
              :selected="i === selectedSuggestion"
              @select="suggestionSelected(i)"
            />
          </div>
        </div>
      </div>
      <div class="actions max-w-full">
        <div :class="{'flex justify-end gap-4 quick-responses mr-4 mb-8 transition-opacity': true, 'opacity-0 pointer-events-none': !currentThreadId, 'opacity-100 pointer-events-all': currentThreadId }">
          <CustomButton
            :class="{'text-xs border hover:bg-lightgray-20': true, 'border-transparent': selectedQuickAction !== i, 'border-primary': selectedQuickAction === i}"
            v-for="(quickResponse, i) in quickResponses"
            @click="selectQuickAction(quickResponse, i)"
            v-text="quickResponse"
          >
          </CustomButton>
        </div>
        <div
          class="grow-0 items-end generate-responses p-4 border border-lightgray rounded-xl flex gap-4">
          <GenerateButton
            @click="generateSuggestions"
            :disabled="selectedSuggestion || !currentThreadId"
          >
            {{ $t('Generate') }}
          </GenerateButton>
          <div
            class="mb-2 max-h-24 overflow-scroll"
          >
            <span v-if="currentThreadId" contenteditable @keyup="messageUpdated" ref="msgInput"
              class="max-w-full text-sm bg-transparent resize-none outline-0 grow-0 text-white block w-full "></span>
          </div>
          <button
            :class="{'outline-0 rounded-xl px-5 py-3 bg-lightgray grow-0 ml-auto': true, 'cursor-not-allowed': messageInput === '', 'bg-primary cursor-pointer': messageInput !== ''}"
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
import GenerateButton from '../global/GenerateButton.vue';
import Stars from '../global/stars.vue';
import ArrowUp from '../global/arrow-up.vue';
import Message from './Message.vue';
import {mapStores} from 'pinia';
import {useMessageStore} from '../../stores/message.js';
import {useThreadStore} from '../../stores/thread.js';
import SuggestService from '../../services/SuggestService.js';
import MessageBody from './MessageBody.vue';
import ThreadService from '../../services/ThreadService';
import MessageService from '../../services/MessageService';

export default {
  name: 'MessageContainer',
  components: {Message, ArrowUp, Stars,GenerateButton, CustomButton, BookmarkOutline, MessageBody},
  props: {
    threadId: {
      type: Number,
    }
  },
  data: () => {
    return {
      selectedSuggestion: null,
      selectedQuickAction: null,
      currentThreadId: null,
      currentThread: null,
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
    async threadId(newVal, oldVal) {
      await this.messageStore.getMessagesForThread(newVal)
      this.suggestions = []
      this.selectedQuickAction = null
      this.selectedSuggestion = null
      this.currentThreadId = newVal
      this.currentThread = this.threadStore.threads.find(t => t.id === this.currentThreadId)
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
    closeSuggestions(){
      this.suggestions = []
    },
    suggestionSelected(i) {
      this.selectedQuickAction = null
      if(this.selectedSuggestion && this.selectedSuggestion === i){
        this.selectedSuggestion = null
        this.insertResponse('')
        return
      }
      this.selectedSuggestion = i
      this.insertResponse(this.suggestions[i])
    },
    async generateSuggestions() {
      if(!this.currentThreadId) {
        return
      }
      const res = await SuggestService.generateSuggestions(this.threadId)
      if(res.status === 200){
        this.suggestions = res.data
      }
    },
    selectQuickAction(message, i) {
      this.selectedQuickAction = i
      this.insertResponse(message)
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
      let selectedSuggestionMessage = null
      if(this.selectedSuggestion && this.suggestions[this.selectedSuggestion] !== this.messageInput){
        selectedSuggestionMessage = this.suggestions[this.selectedSuggestion]
      }
      this.selectedSuggestion = null
      this.selectedQuickAction = null
      this.suggestions = []

      const res = await MessageService.sendMessage(this.currentThreadId, this.messageInput, selectedSuggestionMessage)
      if(res.status === 200){
        this.messageStore.messages[this.currentThreadId].push(message)
        setTimeout(() => {
          this.$refs.messageScroller.scrollTo({top: this.$refs.messageScroller.scrollHeight, behavior: 'smooth'})
          this.messageStore.messages[message.threadId][this.messages[message.threadId].length - 1].state = 'received'
          this.messageInput = ''
          this.$refs.msgInput.innerText = ''
        }, 250)
      }
    },
    async bookmarkThread(){
      const thread = this.threadStore.threads.find(t => t.id === this.currentThreadId)
      const res = await ThreadService.bookmarkThread(this.currentThreadId, !thread.bookmarked)
      if(res.status === 200){
        thread.bookmarked = !thread.bookmarked
      }
    }
  },
  created: function() {

  }
}
</script>

<style lang="scss">
.message-container {
  @media (max-width: 1300px) {
    @apply pr-0;
  }
}
.quick-responses {
  button {
    @apply bg-lightgray text-lightgray-10;
  }
}
.bookmark-button {
  &.bookmarked {
    .bookmark-icon path {
      stroke:  #ACED84;
      fill:  #ACED84;
    }
  }
  .bookmark-icon path {
    @apply transition-all;
  }
  &:hover {
    .bookmark-icon path {
      fill: #494949;
    }
  }
}
</style>
