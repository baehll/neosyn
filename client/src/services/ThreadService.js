import * as API from './API';

export default {
    getThreads(filterOptions, sorting){
        return API.client.post('tbd', {
            filterOptions,
            sorting
        });
    }
}
