import * as API from './API';

export default {
    getThreads(filterOptions, sorting){
        return API.client.post('tbd', {
            filterOptions,
            sorting
        });
    },
    toggleUnreadStatus(id){
        return API.client.patch('tbd', id);
    },
    deleteThread(id){
        return API.client.delete('tbd', id);
    }
}
