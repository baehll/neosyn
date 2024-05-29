<template>
  <div
    :class="{'w-full flex': true, 'justify-begin': from !== null, 'justify-end': from === null, 'opacity-30': state === 'sending'}"
  >
    <div :class="{'flex gap-4 message-wrap': true, 'cursor-pointer': selectable }">
      <div class="flex flex-col ">
        <div class="flex justify-end items-end gap-4 mb-2">
          <p
            @click="$emit('select')"
            :class="{'min-w-16 p-4 border border-lightgray-80 text-white font-roboto text-xs rounded-lg': true,'border border-primary': selected === true, 'bg-lightgray-30': from === null}" v-text="message"
          ></p>
        </div>
        <small v-if="date" :class="{'text-xs text-lightgray-10': true, 'mr-4 self-end': from !== null, 'ml-4 self-begin': from === null}" v-text="getFormattedDate"></small>
        <small v-else-if="messageSubline" :class="{'text-xs text-lightgray-10': true, 'mr-4 self-end': from !== null, 'ml-4 self-begin': from === null}" v-text="messageSubline"></small>
      </div>
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
.message-wrap {
  max-width: 65%;
}
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
