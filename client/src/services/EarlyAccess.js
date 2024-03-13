import * as API from './API';

export default {
    login(password){
        return API.client.post('auth/early_access', {access_key: password});
    }
}