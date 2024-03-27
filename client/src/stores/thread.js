import {defineStore} from 'pinia'
import TimeDifference from '../lib/TimeDifference.js';

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
        async setSetSortingAndFetch() {

        },
        async fetchThreads() {
            // get filters and prepare request
            this.threads =
                [
                    {
                        "id": 1,
                        "platform": "instagram",
                        "last_updated": 1682826686651,
                        "username": "RubyRed",
                        "last_message": "The early bird catches the worm."
                    },
                    {
                        "id": 2,
                        "platform": "facebook",
                        "last_updated": 1649898184408,
                        "username": "MysticFalls",
                        "last_message": "I have a dream."
                    },
                    {
                        "id": 3,
                        "platform": "linkedin",
                        "last_updated": 1707560891353,
                        "username": "AlexTheGreat",
                        "last_message": "Elementary, my dear Watson."
                    },
                    {
                        "id": 4,
                        "platform": "facebook",
                        "last_updated": 1664902126410,
                        "username": "TwilightZone",
                        "last_message": "The early bird catches the worm."
                    },
                    {
                        "id": 5,
                        "platform": "linkedin",
                        "last_updated": 1676615099687,
                        "username": "DaisySunflower",
                        "last_message": "Keep calm and carry on."
                    },
                    {
                        "id": 7,
                        "platform": "whatsapp",
                        "last_updated": 1680258925702,
                        "username": "StormChaser",
                        "last_message": "I have a dream."
                    },
                    {
                        "id": 8,
                        "platform": "instagram",
                        "last_updated": 1656011433474,
                        "username": "FrostByte",
                        "last_message": "Life is like a box of chocolates."
                    },
                    {
                        "id": 10,
                        "platform": "facebook",
                        "last_updated": 1710045369044,
                        "username": "GlimmerStar",
                        "last_message": "I am the master of my fate: I am the captain of my soul."
                    },
                    {
                        "id": 11,
                        "platform": "whatsapp",
                        "last_updated": 1702120952687,
                        "username": "NovaBlast",
                        "last_message": "Where there is love there is life."
                    },
                    {
                        "id": 12,
                        "platform": "whatsapp",
                        "last_updated": 1693554049721,
                        "username": "LunarEclipse",
                        "last_message": "A man is but what he knows."
                    },
                    {
                        "id": 14,
                        "platform": "facebook",
                        "last_updated": 1688692437411,
                        "username": "QuasarLight",
                        "last_message": "Where there is love there is life."
                    },
                    {
                        "id": 18,
                        "platform": "whatsapp",
                        "last_updated": 1666447369148,
                        "username": "OliveBranch",
                        "last_message": "To be or not to be."
                    },
                    {
                        "id": 19,
                        "platform": "instagram",
                        "last_updated": 1708495446264,
                        "username": "EchoBravo",
                        "last_message": "A journey of a thousand miles begins with a single step."
                    }
                ]

            this.lastUpdate = Date.now()
        }
    }
})
