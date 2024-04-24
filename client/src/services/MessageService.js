import * as API from './API';

export default {
    sendMessage(msg) {
       return new Promise((resolve, reject) => {
           const rand = Math.random() * 1900;
           setTimeout(resolve, rand)
       })
      return API.client.post('tbd', {
          threadId: msg.threadId,
          message: msg.message,
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
        return API.client.post('tbd', {
            threadId
        });
    }
}
