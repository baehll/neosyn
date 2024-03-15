<template>
  <div
    @dragover="dragover"
    @dragleave="dragleave"
    @drop="drop"
  >
    <input
      type="file"
      multiple
      name="file"
      id="fileInput"
      class="opacity-0 overflow-hidden absolute w-0.5 h-0.5"
      @change="onChange"
      ref="file"
      accept=".pdf,.jpg,.jpeg,.png"
    />
    <label
      class="hover:cursor-pointer"
      for="fileInput"
    >
      <slot name="drop-info" v-if="isDragging">{{ $t('Drop files here.') }}</slot>
      <slot v-else name="default"></slot>
    </label>
  </div>
</template>
<script>

export default {
  data() {
    return {
      isDragging: false,
      files: [],
    };
  },
  methods: {
    onChange() {
      this.files.push(...this.$refs.file.files);
    },
    dragover(e) {
      console.log('drag');
      e.preventDefault();
      this.isDragging = true;
    },
    dragleave() {
      this.isDragging = false;
    },
    drop(e) {
      e.preventDefault();
      this.$refs.file.files = e.dataTransfer.files;
      this.onChange();
      this.isDragging = false;
    },
  },
  name: 'FileUpload',
  emits: [],
  props: {},
  computed: {},
  mounted: function () {

  },
  created: function () {

  }
}
</script>

<style lang="scss" scoped>

</style>