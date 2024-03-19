<template>
  <div>
    <h2 v-text="$t('Upload your Company\'s Logo')"></h2>
    <p>Lorem ipsum dolor sit amet.</p>
    <div v-if="userStore.companyImageData" class="flex justify-center flex-col items-center">
      <uploaded-image-preview
        class="mb-2"
        :image="userStore.companyImageData"
      />
      <div class="w-64 flex justify-between items-center">
        <FileUpload
          @file-added="companyImageAdded"
        >
          <Button
            tag="a"
            class="outlined"
          >
            {{ $t('Replace') }}
          </Button>
        </FileUpload>
        <Button
          class="outlined"
          @click="deleteImage"
        >
          {{ $t('Delete') }}
        </Button>
      </div>
    </div>
    <FileUpload
      @file-added="companyImageAdded"
      v-if="!userStore.companyImageData"
    >
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

import Button from '../global/CustomButton.vue';
import IdCard from '../IdCard.vue';
import UploadFiles from '../global/upload-files.vue';
import FileUpload from '../global/FileUpload.vue';
import UploadedImagePreview from './UploadedImagePreview.vue';
import {mapStores} from 'pinia';
import {useUserStore} from '../../stores/user.js';

export default {
  emits: ['nextStep', 'prevStep'],
  name: 'Registration Step 1',
  components: {UploadedImagePreview, UploadFiles, IdCard, Button, FileUpload},
  data: () => {
    return {
      imageData: null
    }
  },
  computed: {
    ...mapStores(useUserStore)
  },
  methods: {
    nextStep() {
      this.$emit('nextStep')
    },
    deleteImage(){
      this.userStore.companyImage = ''
      this.userStore.companyImageData = ''
    },
    companyImageAdded(imageArray) {
      const image = imageArray[0];
      this.userStore.companyImage = image
      const reader = new FileReader
      reader.onload = e => {
        this.imageData = e.target.result
        this.userStore.companyImageData = this.imageData;
      }
      reader.readAsDataURL(image)
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>