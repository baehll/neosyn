export const namespaced = true;

export const state = {
    visible: false,
    type: 'success',
    title: '',
    callback: () => {
    },
    message: '',
    timeout: null,
    component: null,
    config: {},
};

export const mutations = {
    SET_TYPE(state, type) {
        state.type = type
    },
    SET_MESSAGE(state, message) {
        state.message = message
    },
    SET_VISIBILITY(state, visibility) {
        if (state.timeout) {
            clearTimeout(state.timeout)
            state.timeout = null
        }
        state.visible = visibility
    },
    SET_TIMEOUT(state, timeout) {
        state.timeout = timeout
    },
    SET_TITLE(state, title) {
        state.title = title
    },
    SET_CALLBACK(state, callback) {
        state.callback = callback
    },
    SET_COMPONENT(state, component) {
        state.component = component
    },
    SET_CONFIG(state, config) {
        state.config = config
    }
};

export const actions = {
    show({commit}, payload) {
        commit('SET_TYPE', payload.type ?? 'success')
        commit('SET_MESSAGE', payload.message)
        commit('SET_TITLE', payload.title)
        commit('SET_CALLBACK', payload.callback)
        commit('SET_COMPONENT', payload.component)
        commit('SET_CONFIG', payload.config)
        commit('SET_VISIBILITY', true)
        commit('SET_TIMEOUT', setTimeout(() => {
            commit('SET_VISIBILITY', false)
        }, 7000))
    },
    showError({commit, dispatch}, payload) {
        dispatch('show', {...payload, type: 'error'})
    },
    hide({commit}) {
        commit('SET_VISIBILITY', false)
    },
    setVisibility({commit}, visibility) {
        commit('SET_VISIBILITY', visibility)
    }
};

export const getters = {
    visible: state => {
        return state.visible
    },
    type: state => {
        return state.type
    },
    message: state => {
        return state.message
    },
    callback: state => {
        return state.callback
    },
    title: state => {
        return state.title
    },
    component: state => {
        return state.component
    },
    config: state => {
        return state.config
    }
};