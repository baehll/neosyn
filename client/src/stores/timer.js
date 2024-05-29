import {defineStore} from 'pinia'
import moment from 'moment';

export const useTimerStore = defineStore('timer', {
    state: () => ({
        now: Date.now(),
    }),
    getters: {
        getTimeDifference: () => pointInTime => {
            const _now = moment()
            const _pointInTime = moment(pointInTime)
            console.log(pointInTime)
            return {
                years: _now.diff(_pointInTime, 'years'),
                months: _now.diff(_pointInTime, 'months'),
                days: _now.diff(_pointInTime, 'days'),
                hours: _now.diff(_pointInTime, 'hours'),
                minutes: _now.diff(_pointInTime, 'minutes'),
                seconds: _now.diff(_pointInTime, 'seconds'),
            }
        }
    },
    actions: {}
})
