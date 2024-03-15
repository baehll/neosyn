import {defineStore} from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        name: '',
        image: '',
        company: '',
    }),
    getters: {
        getName(state) {
            return state.name;
        },
        getImage(state) {
            return state.image;
        },
        getCompany(state) {
            return state.company;
        }
    },
    actions: {
        setName(name) {
            this.name = name;
        },
        setImage(image) {
            this.image = image;
        },
        setCompany(company) {
            this.company = company;
        }
    }
})
