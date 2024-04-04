import {Platform} from './Platforms.js';

export default class {
    static AVAILABLE_PLATFORMS = [
       Platform.Facebook,
       Platform.Instagram
    ]
    selectedPlatforms = []

    constructor(filterOptions){

    }

    addPlatform(platform){
        if(this.selectedPlatforms.indexOf(platform) === -1){
            this.selectedPlatforms.push(platform)
        }
    }

    removePlatform(platform){
        this.selectedPlatforms = this.selectedPlatforms.filter(p => p !== platform)
    }

    getFilterDefinition(){
        const result = {}
        if(this.selectedPlatforms.length){
            result.platforms = this.selectedPlatforms
        }

        return result
    }
}