import * as API from './API';

export default {
    getPlatforms(){
        return API.client.get('/api/supported_platforms');
    }
}
