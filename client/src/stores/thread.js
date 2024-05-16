import {defineStore} from 'pinia'
import ThreadService from '../services/ThreadService.js'


export const useThreadStore = defineStore('thread', {
    state: () => ({
        lastUpdate: null,
        lastUpdateText: '',
        threads: [],
        currentThread: null,
        sorting: 'desc',
        filter: null,
        now: Date.now(),
    }),
    getters: {
        _lastUpdateText: (state) => {
            return $t => {
                const now = Date.now()
                const diff = Math.floor((now - state.lastUpdate) / 1000 / 60)
                const translationMoments = $t('moments ago')
                const translationSingleMinute = $t(':min minute ago').replace(':min', diff)
                const translationMinutes = $t(':min minutes ago').replace(':min', diff)
                let result = translationMoments

                if (diff === 1) {
                    result = translationSingleMinute
                } else if (diff > 1) {
                    result = translationMinutes
                }

                return result
            }
        }
    },
    actions: {
        async markThreadAsUnread(id){
            this.threads.find(t => t.id === id).unread = true
            await ThreadService.toggleUnreadStatus(id, true)
        },
        async markThreadAsRead(id){
            this.threads.find(t => t.id === id).unread = false
            await ThreadService.toggleUnreadStatus(id, false)
        },
        async setSetSortingAndFetch() {

        },
        async fetchThreads() {
            const { data } = await ThreadService.getThreads()
            this.threads = data
            // get filters and prepare request
            // this.threads =
            //     [
            //         {
            //             "unread": true, "id": 1,
            //             "platform": "instagram",
            //             "last_updated": 1682826686651,
            //             "username": "RubyRed",
            //             "last_message": "The early bird catches the worm."
            //         },
            //         {
            //             "bookmark": true,
            //             "unread": true, "id": 2,
            //             "platform": "facebook",
            //             "last_updated": 1649898184408,
            //             "username": "MysticFalls",
            //             "last_message": "I have a dream."
            //         },
            //         {
            //             "unread": true, "id": 3,
            //             "platform": "linkedin",
            //             "last_updated": 1707560891353,
            //             "username": "AlexTheGreat",
            //             "last_message": "Elementary, my dear Watson."
            //         },
            //         {
            //             "unread": true, "id": 4,
            //             "platform": "facebook",
            //             "last_updated": 1664902126410,
            //             "username": "TwilightZone",
            //             "last_message": "The early bird catches the worm."
            //         },
            //         {
            //             "unread": true, "id": 5,
            //             "platform": "linkedin",
            //             "last_updated": 1676615099687,
            //             "username": "DaisySunflower",
            //             "last_message": "Keep calm and carry on."
            //         },
            //         {
            //             "unread": false, "id": 7,
            //             "platform": "facebook",
            //             "last_updated": 1680258925702,
            //             "username": "StormChaser",
            //             "last_message": "I have a dream."
            //         },
            //         {
            //             "unread": false, "id": 8,
            //             "platform": "instagram",
            //             "last_updated": 1656011433474,
            //             "username": "FrostByte",
            //             "last_message": "Life is like a box of chocolates."
            //         },
            //         {
            //             "unread": false, "id": 10,
            //             "platform": "facebook",
            //             "last_updated": 1710045369044,
            //             "username": "GlimmerStar",
            //             "last_message": "I am the master of my fate: I am the captain of my soul."
            //         },
            //         {
            //             "unread": true, "id": 11,
            //             "platform": "facebook",
            //             "last_updated": 1702120952687,
            //             "username": "NovaBlast",
            //             "last_message": "Where there is love there is life."
            //         },
            //         {
            //             "unread": true, "id": 12,
            //             "platform": "facebook",
            //             "last_updated": 1693554049721,
            //             "username": "LunarEclipse",
            //             "last_message": "A man is but what he knows."
            //         },
            //         {
            //             "unread": false, "id": 14,
            //             "platform": "facebook",
            //             "last_updated": 1688692437411,
            //             "username": "QuasarLight",
            //             "last_message": "Where there is love there is life."
            //         },
            //         {
            //             "unread": false, "id": 18,
            //             "platform": "facebook",
            //             "last_updated": 1666447369148,
            //             "username": "OliveBranch",
            //             "last_message": "To be or not to be."
            //         },
            //         {
            //             "unread": true, "id": 19,
            //             "platform": "instagram",
            //             "last_updated": 1708495446264,
            //             "username": "EchoBravo",
            //             "last_message": "A journey of a thousand miles begins with a single step."
            //         }
            //     ]
            //
            this.lastUpdate = Date.now()
        }
    }
})
