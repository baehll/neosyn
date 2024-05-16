import * as API from './API';

export default {
    generateSuggestions: (threadId) => {
        return API.client.post(`/api/data/ai/generate_responses`, {
            threadId
        })
    }
}
