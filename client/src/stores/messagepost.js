import {defineStore} from 'pinia'
import MessagePostService from '../services/MessageService.js';

export const useMessagePostStore = defineStore('messagePost', {
    state: () => ({
        messagePosts: [
            {
//                 content: 'ARE YOU READY? 🤤Nur noch 7 TAGE und eure creamy dreams werden wahr 🫠Am Dienstag launchen wir exklusiv in
//           unserem Onlineshop einen neuen nucao Schokoriegel! 💥So viel vorweg: Es wird extreeeeem cremig, nussig und sau
//           lecker.Welche Riegelsorte wird es wohl werden? 👀Unter allen Antworten in den Kommentaren verlosen wir zweimal
//           eine 12er Packung der neuen Sorte!Ratet bis zum 12.10.2023, 18 Uhr und probiert als erstes unseren neuen Riegel!
//           .
//           .
//           .
//           .
//           .
//           .
//           .
//           .
//           .
//           .
//           #Lorem #Ipsum #Dolor
// '
            }
        ]
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
