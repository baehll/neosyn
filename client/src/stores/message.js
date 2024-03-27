import {defineStore} from 'pinia'

export const useMessageStore = defineStore('message', {
    state: () => ({
        messages: {},
        currentMessages: [],
    }),
    getters: {},
    actions: {
        /**
         * Sets the current thread id and fetches the messages from this thread
         * @param state
         * @param threadId
         */
        getMessagesForThread(state, threadId) {

        }
    }
})
