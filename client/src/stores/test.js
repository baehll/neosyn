import {defineStore} from 'pinia'

export const useTestStore = defineStore('test', {
    state: () => ({
        files: []
    }),
    getters: {
        getFiles: state => {
            return state.files
        }
    },
    actions: {
        bla: () => {
            console.log('bla');
        }
    }
})
