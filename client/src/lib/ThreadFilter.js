import {Platform} from './Platforms.js';
import { Message } from './Message.js';
export default class {
    static AVAILABLE_PLATFORMS = [
       Platform.Instagram,
       Platform.Facebook,
       Platform.WhatsApp,
       Platform.LinkedIn,
       Platform.YouTube,
       Platform.X,
    ]

    static MESSAGE_TYPES = [
        Message.QUESTION,
        Message.POSITIVE,
        Message.NEGATIVE,
        Message.NEUTRAL,
    ]
    selectedPlatforms = []
    selectedMessageTypes = []

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

    addMessageType(messageType){
        if(this.selectedMessageTypes.indexOf(messageType) === -1){
            this.selectedMessageTypes.push(messageType)
        }
    }

    removeMessageType(messageType){
        this.selectedMessageTypes = this.selectedMessageTypes.filter(m => m !== messageType)
    }

    getFilterDefinition(){
        const result = {}
        if(this.selectedPlatforms.length){
            result.platforms = this.selectedPlatforms
        }

        if(this.selectedMessageTypes.length){
            result.messageTypes = this.selectedMessageTypes
        }

        return result
    }
}
