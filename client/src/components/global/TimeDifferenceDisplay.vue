<template>
<span v-text="difference"></span>
</template>
<script>

import {mapStores} from 'pinia';
import {useTimerStore} from '../../stores/timer.js';

export default {
  name: 'TimeDifferenceDisplay',
  emits: [],
  props: {
    pointInTime: {
      type: Number
    }
  },
  data: () => {
    return {}
  },
  computed: {
    ...mapStores(useTimerStore),
    difference() {
      const now = this.timerStore.now
      const res = this.timerStore.getTimeDifference(this.pointInTime)
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
  methods: {},
  mounted: function () {

  },
  created: function () {

  }
}
</script>

<style lang="scss" scoped>

</style>