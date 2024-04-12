<template>
    <div :class="{'w-5/12 flex gap-4 justify-end': true,  'cursor-pointer': selectable }">
      <div class="flex flex-col ">
        <div class="flex justify-end items-end gap-4 mb-2">
          <div
            v-if="from !== 0"
            class="bg-primary rounded-full w-8 h-8 shrink-0">
          </div>
          <p
            @click="$emit('select')"
            :class="{'p-4 border border-lightgray-80 text-white font-roboto text-xs rounded-lg': true,'border border-primary': selected === true, 'bg-lightgray-30': from === 0}" v-text="message"
          ></p>
        </div>
        <small v-if="date" :class="{'text-xs text-lightgray-10': true, 'mr-4 self-end': from !== 0, 'ml-4 self-begin': from === 0}" v-text="getFormattedDate"></small>
        <small v-else-if="messageSubline" :class="{'text-xs text-lightgray-10': true, 'mr-4 self-end': from !== 0, 'ml-4 self-begin': from === 0}" v-text="messageSubline"></small>
      </div>
    </div>
</template>
<script>

import moment from 'moment';

export default {
  components: {},
  emits: ['select'],
  props: {
    selectable: {
      type: Boolean,
      default: false
   },
    selected: {
      type: Boolean,
    },
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
    state: {
      type: String,
      default: 'received'
    },
    id: {
      type: Number,
    },
    messageSubline: {
      type: String,
    }
  },
  data: () => {
    return {}
  },
  computed: {
    getFormattedDate() {
      return moment(this.date).format(this.$i18n.t('dateTimeFormat'))
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
  font-size: 10px;
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
