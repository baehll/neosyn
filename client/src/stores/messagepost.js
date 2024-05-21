import {defineStore} from 'pinia'
import MessagePostService from '../services/MessagePostService.js'

export const useMessagePostStore = defineStore('messagePost', {
    state: () => ({
        messagePosts: [],
    }),
    getters: {},
    actions: {
        async getPostForThread(threadId) {
            let post = this.messagePosts.find(i => i.threadId === threadId)
            if(!post) {
                const {data} = await MessagePostService.getPostForThread(threadId)
                post = data
                this.messagePosts.push(post)
            }
            return post
        }
    }
})
