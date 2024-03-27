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
         * @param threadId
         */
        getMessagesForThread(threadId) {
            this.messages = {
                1: [
                    {
                        id: 1,
                        from: 1,
                        message: 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
                        date: new Date(),
                    },
                    {
                        id: 2,
                        from: 0,
                        message: 'Lorem ipsum antwort',
                        date: new Date(),
                    },

                ]
            }
        }
    }
})
