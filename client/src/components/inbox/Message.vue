<template>
  <div :class="{'my-1': true, 'text-primary': from_id !== id, 'text-light': from_id === id}">
    <small class="block w-full text-center font-teko-light text-light mb-1" v-text="date"></small>
    <template v-if="showLogo && logo">
      <div class="flex gap-x-1 items-center">
        <div class="logo">
          <img :src="logo" width="26" height="26"/>
        </div>
        <p v-text="body" class="leading-relaxed font-ubuntu-regular"></p>
      </div>
    </template>
    <template v-else>
      <p class="body font-ubuntu-regular leading-relaxed" v-text="body"></p>
    </template>
  </div>
</template>
<script>

export default {
  components: {},
  props: {
    body: {
      type: String
    },
    from: {
      type: String
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
    from_id: {
      type: String
    }
  },
  data: () => {
    return {}
  },
  computed: {
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
