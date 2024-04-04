import * as API from './API';

export default {
    getMessages(threadId){
        return API.client.post('tbd', {
            threadId
        });
    }
}
