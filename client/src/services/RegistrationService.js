import * as API from './API';

export default {
    register(name, companyName, logo){
        const form = new FormData
        form.append('username', name)
        form.append('companyname', companyName)
        if(logo){
            form.append('file', logo)
        }
        return API.client.post('/api/init_user', form, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
    }
}
