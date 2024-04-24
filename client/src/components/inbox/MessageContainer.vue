<template>
  <div class="grow overflow-hidden h-full px-5 py-5 bg-lightgray">
    <div class="overflow-hidden flex flex-col justify-between w-full h-full bg-darkgray rounded-xl message p-4">
      <div class="flex justify-between px-2 pt-2 pb-4">
        <span class="rounded-3xl border border-white px-4 text-white py-1" v-text="$t('Interaction')"></span>
        <button
          :class="{'bookmark-button': true, 'bookmarked': currentThread && currentThread.bookmark}"
          @click="bookmarkThread"
        >
          <BookmarkOutline
            class="bookmark-icon custom-fill"
          />
        </button>
      </div>
      <div class="messages flex-grow relative">
        <div
          class="pl-2 pr-5 pt-4 pb-6 messages items-start flex flex-col h-full overflow-scroll absolute top-0 left-0 "
          ref="messageScroller">
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
              :message="suggestion.message"
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
      this.selectedQuickAction = null
      this.selectedSuggestion = null
      this.currentThreadId = newVal
      this.messageInput = ''
      setTimeout(() => {
        this.$refs.messageScroller.scrollTo({top: this.$refs.messageScroller.scrollHeight, behavior: 'smooth'})
      }, 250)
    }
  },
  computed: {
    ...mapStores(useThreadStore, useMessageStore),
    currentThread(){
      return this.threadStore.threads[this.currentThreadId] || null
    }
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
      this.insertResponse(this.suggestions[i].message)
    },
    async generateSuggestions() {
      if(!this.currentThreadId) {
        return
      }
      this.suggestions = await SuggestService.generateSuggestions(this.threadId)
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
      this.selectedSuggestion = null
      this.selectedQuickAction = null
      this.suggestions = []
      this.messageStore.messages[this.currentThreadId].push(message)
      setTimeout(() => {
        this.$refs.messageScroller.scrollTo({top: this.$refs.messageScroller.scrollHeight, behavior: 'smooth'})
        this.messageStore.sendMessage(message)
        this.messageInput = ''
        this.$refs.msgInput.innerText = ''
      }, 250)
    },
    bookmarkThread(){
      this.threadStore.threads[this.currentThreadId].bookmark = !this.threadStore.threads[this.currentThreadId].bookmark
    }
  },
  created: function() {

  }
}
</script>

<style lang="scss">
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
