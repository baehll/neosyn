<template>
<span v-text="diff"></span>
</template>
<script>

import {mapStores} from 'pinia';
import {useTimerStore} from '../../stores/timer.js';
import moment from 'moment'

export default {
  name: 'TimeDifferenceDisplay',
  emits: [],
  props: {
    pointInTime: {
      type: Number
    },
    now: {
      type: Number
    },
  },
  data: () => {
    return {
      diff: null
    }
  },
  watch: {
    now(newVal, oldVal){
      this.diff = this.difference()
    }
  },
  computed: {
    ...mapStores(useTimerStore),
  },
  methods: {
    difference() {
      const _now = moment()
      const _pointInTime = moment(this.pointInTime)
      const res = {
        years: _now.diff(_pointInTime, 'years'),
        months: _now.diff(_pointInTime, 'months'),
        days: _now.diff(_pointInTime, 'days'),
        hours: _now.diff(_pointInTime, 'hours'),
        minutes: _now.diff(_pointInTime, 'minutes'),
        seconds: _now.diff(_pointInTime, 'seconds'),
      }
      const {years, months, days, hours, minutes} = res
      const translations = {
        defaultTranslation: this.$i18n.t('moments ago'),
        years: {
          single: this.$i18n.t(':time year ago').replace(':time', years),
          plural: this.$i18n.t(':time years ago').replace(':time', years),
        },
        months: {
          single: this.$i18n.t(':time month ago').replace(':time', months),
          plural: this.$i18n.t(':time months ago').replace(':time', months),
        },
        days: {
          single: this.$i18n.t(':time day ago').replace(':time', days),
          plural: this.$i18n.t(':time days ago').replace(':time', days),
        },
        hours: {
          single: this.$i18n.t(':time hour ago').replace(':time', hours),
          plural: this.$i18n.t(':time hours ago').replace(':time', hours),
        },
        minutes: {
          plural: this.$i18n.t(':time minutes ago').replace(':time', minutes),
          single: this.$i18n.t(':time minute ago').replace(':time', minutes),
        },
      }
      const timespans = ['years', 'months', 'days', 'hours', 'minutes']
      for(const timespan of timespans){
        if(res[timespan] !== 0){
          return res[timespan] === 1 ? translations[timespan].single : translations[timespan].plural
        }
      }
      return translations.defaultTranslation
    }
  },
  mounted: function () {

  },
  created: function () {
    this.diff = this.difference()
  }
}
</script>

<style lang="scss" scoped>

</style>
