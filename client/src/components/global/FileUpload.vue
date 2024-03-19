<template>
  <div
    @dragover="dragover"
    @dragleave="dragleave"
    @drop="drop"
  >
    <input
      :multiple="multiple"
      type="file"
      name="file"
      :id="`fileInput-${uuid}`"
      class="opacity-0 overflow-hidden absolute w-0.5 h-0.5"
      @change="onChange"
      ref="file"
      accept=".pdf,.jpg,.jpeg,.png"
    />
    <label
      class="hover:cursor-pointer"
      :for="`fileInput-${uuid}`"
    >
      <slot name="drop-info" v-if="isDragging">{{ $t('Drop files here.') }}</slot>
      <slot v-else name="default"></slot>
    </label>
  </div>
</template>
<script>

import {mapStores} from 'pinia';
import {useFileStore} from '../../stores/file.js';
import {useTestStore} from '../../stores/test.js';

export default {
  data() {
    return {
      uuid: Date.now(),
      isDragging: false,
      files: [],
    };
  },
  methods: {
    onChange() {
      this.$emit('file-added', this.$refs.file.files)
      this.filesStore.files.push(...this.$refs.file.files);
    },
    dragover(e) {
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
  emits: ['file-added'],
  props: {
    multiple: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapStores(useFileStore, useTestStore)
  },
  mounted: function () {

  },
  created: function () {
  }
}
</script>

<style lang="scss" scoped>

</style>