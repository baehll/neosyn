import * as API from './API';

export default {
    sendMessage(message, generated_message) {
      return API.client.post(`/api/data/threads/${msg.threadId}/message`, {
            message,
            generated_message
      })
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
