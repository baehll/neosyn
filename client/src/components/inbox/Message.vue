<template>
  <div :class="{'w-full flex': true, 'justify-begin': from !== 0, 'justify-end': from === 0}">
    <div class="w-5/12 flex gap-4 justify-end">
      <div class="flex flex-col ">
        <div class="flex items-end gap-4 mb-2">
          <div
            v-if="from !== 0"
            class="bg-primary rounded-full w-8 h-8 shrink-0">
          </div>
          <p class="p-4 border border-lightgray text-lightgray-90 rounded-lg" v-text="message"></p>
        </div>
        <small :class="{'text-lightgray-90': true, 'self-end': from !== 0, 'self-begin': from === 0}" v-text="getFormattedDate"></small>
      </div>
    </div>
  </div>
</template>
<script>

import moment from 'moment';

export default {
  components: {},
  props: {
    message: {
      type: String
    },
    from: {
      type: Number,
    },
    logo: {
      type: String,
    },
    date: {
      type: String
    },
    isNew: {
      type: Boolean
    },
    showLogo: {
      type: Boolean,
      default: false
    },
    id: {
      type: Number,
    }
  },
  data: () => {
    return {}
  },
  computed: {
    getFormattedDate() {
      return moment(this.date).format(this.$i18n.t('dateFormat'))
    },
    getThreads() {

    },
    getClass() {
      return this.id === this.from_id
    }
  },
  methods: {},
  async created() {

  }
}
</script>
<style lang="scss" scoped>
.body {
  @apply pl-1;
  margin-left: 26px;
}

small {
  font-size: 14px;
}

p {
  font-size: 14px;
}

.logo {
  @apply rounded-full overflow-hidden bg-white flex items-center justify-center;
  width: 26px;
  height: 26px;

  img {
    @apply rounded-full;
  }
}
</style>
