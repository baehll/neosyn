import { createStore } from 'vuex'
import modules from './modules'

const debug = process.env.NODE_ENV !== 'production'

export default createStore({
    modules,
    strict: debug,
})
