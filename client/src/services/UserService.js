import * as API from './API';

export default {
    me: () => {
        return API.client.get(`/api/me`)
    }
}
