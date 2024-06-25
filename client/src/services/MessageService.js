import * as API from './API';

export default {
    sendMessage(threadId, message, generated_message) {
        const payload = {
            message
        }
        if (generated_message && message !== generated_message){
            payload['generated_message'] = generated_message
        }
        return API.client.post(`/api/data/threads/${threadId}/message`, payload)
    },

    /**
    * Returns messages for a thread
    * Data structure:
    *
    * [
    *   {
    *       id int,
    *       threadId int,
    *       content string,
    *       from int,
    *       messageDate datetime,
    *   }
    * ]
    *
    */
    getMessages(threadId){
        return API.client.get(`/api/data/threads/${threadId}`)
    }
}
