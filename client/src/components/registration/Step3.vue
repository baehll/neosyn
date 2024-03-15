<template>
  <div>
    <h2 v-text="$t('Upload your Company\'s Logo')"></h2>
    <p>Lorem ipsum dolor sit amet.</p>
    <FileUpload>
      <template v-slot:drop-info>
        <div class="border border-lightgray rounded py-36 w-full flex justify-center items-center flex-col">
          <div class="flex flex-col items-center justify-center">
            <upload-files
              class="text-lightgray-10 mb-4"
            />
            <p class="text-xs text-lightgray-10" v-text="$t('Drop files here.')"></p>
          </div>
        </div>
      </template>
      <div class="border border-lightgray rounded py-36 w-full flex justify-center items-center flex-col">
        <div class="flex flex-col items-center justify-center">
          <upload-files
            class="text-lightgray-10 mb-4"
          />
          <p class="text-xs text-lightgray-10" v-text="$t('Upload files')"></p>
        </div>
      </div>
    </FileUpload>
  </div>
</template>
<script>

import Button from '../global/Button.vue';
import IdCard from '../IdCard.vue';
import UploadFiles from '../global/upload-files.vue';
import FileUpload from '../global/FileUpload.vue';

export default {
  emits: ['nextStep', 'prevStep'],
  name: 'Registration Step 1',
  components: {UploadFiles, IdCard, Button, FileUpload},
  data: () => {
    return {}
  },
  computed: {},
  methods: {
    nextStep() {
      this.$emit('nextStep')
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>