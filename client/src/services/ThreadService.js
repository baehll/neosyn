import * as API from './API';

export default {
    /**
     * Returns threads based on filter options and sorting
     * Data structure:
     * [
     *      {
     *          id int,
     *          username string,
     *          message string,
     *          platform int/string,
     *          lastUpdated datetime,
     *          unread bool,
     *      }
     * ]
     *
     * Data structure for filterOptions:
     * {
     *      platforms: [int/string],
     *      sentiments: [int/string] (question, positive, neutral, negative),
     * }
     *
     * Data structure for sorting:
     * Value of new, most-interaction, old or least-interaction
     */
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
