import {defineStore} from 'pinia'
import MessageService from '../services/MessageService.js';

export const useMessageStore = defineStore('message', {
    state: () => ({
        messages: {},
        currentMessages: [],
    }),
    getters: {},
    actions: {
        async sendMessage(message) {
            // first send the message
            try {
                const res = await MessageService.sendMessage(message)
                this.messages[message.threadId][this.messages[message.threadId].length - 1].state = 'received'
                // if we get a successful response from the server, mark it as sent
            } catch (e) {
                console.log(e);
            }
        },
        /**
         * Sets the current thread id and fetches the messages from this thread
         * @param threadId
         */
        async getMessagesForThread(threadId) {
            const { data } = await MessageService.getMessages(threadId)
            this.messages[threadId] = data
            return this.messages[threadId]
        }
    }
})
