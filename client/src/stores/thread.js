import {defineStore} from 'pinia'
import ThreadService from '../services/ThreadService.js'


export const useThreadStore = defineStore('thread', {
    state: () => ({
        lastUpdate: Date.now(),
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
        async fetchThreads(filter = null, searchTerm = null, sorting = null, offset = null) {
            const { data } = await ThreadService.getThreads(filter, searchTerm, sorting, offset)
            this.threads = data
            this.lastUpdate = Date.now()
        },
    }
})
