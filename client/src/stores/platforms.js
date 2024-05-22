import {defineStore} from 'pinia'
import PlatformService from '../services/PlatformService.js'

export const usePlatformStore = defineStore('platform', {
    state: () => ({
        platforms: []
    }),
    getters: {},
    actions: {
        getPlatforms: async function() {
            const { data } = await PlatformService.getPlatforms()
            this.platforms = data
        }
    }
})
