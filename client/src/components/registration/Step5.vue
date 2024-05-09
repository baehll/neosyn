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
      <div :class="{'border border-lightgray rounded min-h-72 w-full flex': true,' justify-center items-center flex-col': !uploadedFiles.length, 'flex-row gap-2 p-4': uploadedFiles.length}">
        <div :class="{ 'flex flex-col items-center justify-center': !uploadedFiles.length, 'w-full': uploadedFiles.length }">
          <upload-files
            v-if="uploadedFiles.length === 0"
            class="text-lightgray-60 mb-4"
          />
          <p
            v-if="uploadedFiles.length === 0"
            class="text-xs text-lightgray-90 text-center"
          >
            {{$t('Upload files')}}
            <small class="text-darkgray-80 block">{{$t('.csv, .docx, .html, .json, .md, .pdf, .pptx, .tex, .txt')}}</small>
          </p>
          <ul class="flex flex-wrap gap-2">
            <li
              class="w-1/4"
              v-for="file in uploadedFiles"
            >
              <UploadedFile
              @delete-file="removeFileFromList"
                :filename="file.name"
              />
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
import UploadedFile from './UploadedFile.vue';


export default {
  emits: ['nextStep', 'prevStep'],
  name: 'Registration Step 1',
  components: {UploadFiles, FileUpload, IdCard, Button, UploadedFile},
  data: () => {
    return {
      uploadedFiles: []
    }
  },
  computed: {
    ...mapStores(useUserStore)
  },
  methods: {
    removeFileFromList(filename){
      this.uploadedFiles = this.uploadedFiles.filter(f => f.name !== filename)
    },
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
