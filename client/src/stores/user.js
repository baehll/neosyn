import {defineStore} from 'pinia'
import UserService from '../services/UserService.js';

export const useUserStore = defineStore('user', {
    state: () => ({
        name: '',
        companyImage: '',
        companyImageData: '',
        company: '',
        companyFiles: [],
        userInfo: {},
        logoUrl: null,
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
        },
        getCompanyFiles(state){
            return state.companyFiles
        },
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
        },
        async me(){
            const {data} = await UserService.me()
            const {name, companyName, logoURL} = data
            this.name = name
            this.companyName = companyName
            this.logoUrl = logoURL
        }
    }
})
