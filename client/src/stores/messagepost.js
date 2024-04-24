import {defineStore} from 'pinia'
import MessagePostService from '../services/MessageService.js';

export const useMessagePostStore = defineStore('messagePost', {
    state: () => ({
        messagePosts: []
    }),
    getters: {},
    actions: {
        async getPostForThread(threadId) {
            let post = this.messagePosts.find(i => i.id === threadId)
            if(!post) {
                post = await MessagePostService.getPostForThread(threadId)
                this.messagePosts.push(post)
            }
            return post
        }
    }
})
