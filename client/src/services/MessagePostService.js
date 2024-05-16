import * as API from './API';

export default {
    /**
     * Returns the social media post for a given thread id
     * Data structure:
     * {
     *      id int,
     *      threadId int,
     *      postMedia string (absolute url),
     *      postMediaType string (image, video)
     *      postContent string (post caption),
     *      platform (either id referencing the different socialmedia platforms
     *      in another table or string, eg. facebook),
     *      likes int,
     *      comments int,
     *      shares int
     * }
     */
    async getPostForThread(threadId){
        return API.client.get(`/api/data/threads/${threadId}/post`)
    }
}
