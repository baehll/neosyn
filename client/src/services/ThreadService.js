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
    getThreads(filterOptions, searchTerm, sorting, offset){
        let apiUrl = '/api/data/threads/'
        const paramsToAdd = []
        const urlParams = {
            sorting,
            offset
        }

        for(const paramName in urlParams){
            if(urlParams[paramName]){
                paramsToAdd.push(`${paramName}=${urlParams[paramName]}`)
            }
        }

        if(paramsToAdd.length){
            const joinedParams = paramsToAdd.join('&')
            apiUrl += `?${joinedParams}`
        }

        return API.client.post(apiUrl, {
            platforms: filterOptions.platform,
            sentiments: filterOptions.sentiment,
            q: searchTerm,
        });
    },
    toggleUnreadStatus(id, unread){
        return API.client.put(`/api/data/threads/${id}`, {
            unread
        });
    },
    deleteThread(id){
        return API.client.delete('tbd', id);
    },
    bookmarkThread(id, bookmarked){
        return API.client.put(`/api/data/threads/bookmarks/${id}`, {
            bookmarked
        })
    }
}
