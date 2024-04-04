<template>
  <div class="flex items-center flex-col">
    <div
      class="w-64 h-64 rounded-full bg-black border border-lightgray-80 bg-contain"
      :style="{ 'background-image': `url(${image})` }"
    >
    </div>
  </div>
</template>
<script>

export default {
  name: 'UploadedImagePreview',
  emits: [],
  props: {
    image: {
      type: String,
      default: ''
    }
  },
  data: () => {
    return {
      imageData: null,
    }
  },
  computed: {

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