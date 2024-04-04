import {defineStore} from 'pinia'

export const useFileStore = defineStore('files', {
    state: () => ({
        files: [],
        imageData: null,
    }),
    getters: {
        getFiles: state => {
            return state.files
        },
        getFirstFileData: (state) => () => {
            const file = state.files[0]

        }
    },
    actions: {
        test: (state, action) => {
            return true
        }
    }
})
