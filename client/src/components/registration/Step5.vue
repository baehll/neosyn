<template>
  <div>
    <h2 v-text="$t('Please provide more information about your company.')"></h2>
    <p v-text="$t('Drag and drop relevant Information about your Company e.g. corporate language guidelines and product information sheets.')"></p>

    <FileUpload
      accepted-files=".pdf,.docx,.csv,.html,.json,.md,.pptx,.tex,.txt"
      @file-added="companyFileAdded"
    >
      <template v-slot:drop-info>
        <div class="border border-lightgray rounded py-36 w-full flex justify-center items-center flex-col">
          <div class="flex flex-col items-center justify-center">
            <upload-files
              class="text-lightgray-60 mb-4"
            />
            <p class="text-xs text-lightgray-90 text-center">
              {{$t('Upload files')}}
              <small class="text-darkgray-80 block">{{$t('.csv, .docx, .html, .json, .md, .pdf, .pptx, .tex, .txt')}}</small>
            </p>
          </div>
        </div>
      </template>
      <div class="border border-lightgray rounded py-36 w-full flex justify-center items-center flex-col">
        <div class="flex flex-col items-center justify-center">
          <upload-files
            class="text-lightgray-60 mb-4"
          />
          <p v-if="uploadedFiles.length === 0" class="text-xs text-lightgray-90 text-center">
            {{$t('Upload files')}}
            <small class="text-darkgray-80 block">{{$t('.csv, .docx, .html, .json, .md, .pdf, .pptx, .tex, .txt')}}</small>
          </p>
          <ul>
            <li v-for="file in uploadedFiles">
              {{file.name}}
            </li>
          </ul>
        </div>
      </div>
    </FileUpload>  </div>
</template>
<script>

import Button from '../global/CustomButton.vue';
import IdCard from '../IdCard.vue';
import {useUserStore} from '../../stores/user.js';
import {mapStores} from 'pinia';
import FileUpload from '../global/FileUpload.vue';
import UploadFiles from '../global/upload-files.vue';

export default {
  emits: ['nextStep', 'prevStep'],
  name: 'Registration Step 1',
  components: {UploadFiles, FileUpload, IdCard, Button},
  data: () => {
    return {
      uploadedFiles: []
    }
  },
  computed: {
    ...mapStores(useUserStore)
  },
  methods: {
    nextStep() {
      this.$emit('nextStep')
    },
    companyFileAdded(files) {
      this.uploadedFiles.push(...files)
      console.log(this.uploadedFiles);
      this.userStore.companyFiles = this.uploadedFiles
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>
