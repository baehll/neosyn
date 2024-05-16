<template>
  <div class="registration flex flex-row h-full">
    <div class="flex flex-col justify-between basis-1/3 bg-darkgray p-8 text-white">
      <div>
        <Button
          :class="{ 'icon-only transition-opacity': true, 'opacity-0 invisible': currentStep === 0, 'opacity-100': currentStep > 0 }"
          @click="previousStep">
          <chevron-left class="w-5 mb-10" />
        </Button>

        <transition name="fade-left" mode="out-in">
          <component :key="currentStep" v-if="currentStepComponent" :is="currentStepComponent" @nextStep="nextStep" />
        </transition>
      </div>
      <div class="flex flex-row justify-between items-center">
        <ProgressBar class="basis-1/4" :percentage="(currentStep + 1) / ((steps.length) / 100)" />
        <div>
          <Button class="ghost" @click="finishRegistrationWithoutFileUpload" v-if="steps[currentStep].finishRegistration">
            {{ $t('Later') }}
          </Button>
          <Button class="ghost" @click="skipStep" v-if="steps[currentStep].hasSkipOption">
            {{ $t('Skip') }}
          </Button>
          <Button class="basis-1/4 bg-lightgray-60 text-darkgray" :disabled="!isValid"
                  v-if="currentStep < steps.length - 1" @click="nextStep">
            {{ $t('Continue') }}
          </Button>
          <Button class="basis-1/4" v-if="currentStep === steps.length - 1" :disabled="!isValid" @click="finishRegistration">
            {{ $t('Continue') }}
          </Button>
        </div>
      </div>
    </div>

    <div class="relative basis-2/3 bg-lightgray flex items-center justify-center">
      <div class="absolute w-full h-full top-0 left-0">

      </div>
      <IdCard
        v-if="currentStep < steps.length - 1"
      />
      <UploadProgressIndicator
        v-if="currentStep === steps.length - 1"
        :upload-started="uploadStarted"
      />
    </div>
    <Logo class="absolute top-8 right-8 w-28 h-28 header-left text-lightgray-10" />
  </div>
</template>
<script>

import ProgressBar from './components/global/ProgressBar.vue';
import Step1 from './components/registration/Step1.vue';
import Button from './components/global/CustomButton.vue';
import IdCard from './components/IdCard.vue';
import Step2 from './components/registration/Step2.vue';
import ChevronLeft from './components/global/chevron-left.vue';
import Step3 from './components/registration/Step3.vue';
import { mapStores } from 'pinia';
import { useUserStore } from './stores/user.js';
import Step4 from './components/registration/Step4.vue';
import Logo from './components/global/logo.vue';
import Step5 from './components/registration/Step5.vue';
import RegistrationService from './services/RegistrationService';
import UploadProgressIndicator from './components/registration/UploadProgressIndicator.vue';

export default {
  name: 'Registration',
  components: {
    UploadProgressIndicator,
    Logo,
    ChevronLeft,
    IdCard,
    Button,
    ProgressBar
  },
  data: () => {
    return {
      uploadStarted: false,
      steps: [
        {
          component: Step1,
          validation: (store) => {
            return store.name.trim() !== ''
          }
        },
        {
          component: Step2,
          validation: (store) => {
            return store.company.trim() !== ''
          }
        },
        {
          component: Step3,
          hasSkipOption: true,
          validation: () => {
            return true
          }
        },
        {
          component: Step4,
          validation: () => {
            return true
          }
        },
        {
          component: Step5,
          finishRegistration: true,
          validation: (store) => {
            return store.companyFiles.length
          }
        },
      ],
      currentStepComponent: Step1,
      currentStep: 0
    }
  },
  computed: {
    ...mapStores(useUserStore),
    isValid() {
      return this.steps[this.currentStep].validation(this.userStore)
    },
  },
  methods: {
    async skipStep() {
      if (this.currentStep === this.steps.length - 1) {
        return
      }

      this.currentStep++;
      this.currentStepComponent = this.steps[this.currentStep].component;
    },
    async nextStep() {
      if (this.currentStep === this.steps.length - 1) {
        return
      }

      if(this.currentStep === 2){
        const res = await RegistrationService.register(this.userStore.name, this.userStore.company, this.userStore.companyImage)
        if(res.status > 300){
          // show error message
        }
      }

      this.currentStep++;
      this.currentStepComponent = this.steps[this.currentStep].component;
    },
    previousStep() {
      if (this.currentStep === 0) {
        return
      }
      this.currentStep--;
      this.currentStepComponent = this.steps[this.currentStep].component;
    },
    finishRegistrationWithoutFileUpload(){
      window.location = '/app.html'
    },
    async finishRegistration() {
      this.uploadStarted = true
      const res = await RegistrationService.companyFiles(this.userStore.companyFiles)
      this.uploadStarted = false
      if(res.status > 300){
        // show error
      }
      this.finishRegistrationWithoutFileUpload()
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
html{
  #app {
    height: 100vh;
  }

  @media (min-width: 1024px) and (max-width: 1530px) {
    -moz-transform: scale(0.8, 0.8);
    -ms-transform: scale(0.8);
    -webkit-transform: scale(0.8);
    transform: scale(0.8);

    width:125%; /* to compensate for the 0.8 scale */
    transform-origin:0 0; /* to move it back to the top left of the window */
    #app {
      height: 125vh;
    }
  }
}
.registration {
  p {
    @apply mb-8;
  }

  h2 {
    @apply mb-4;
    font-size: 42px;
    line-height: 1.2;
  }

  input {
    @apply border border-lightgray focus:border-primary ring-0 focus:outline-0 outline-0 focus:ring-0 focus:ring-offset-0 rounded-lg w-full bg-transparent py-2 px-4;
  }

  label {
    p {
      @apply mb-0;
    }
  }
}

.fade-left-enter-active,
.fade-left-leave-active {
  transition: opacity 0.5s ease;
}

.fade-left-enter-from,
.fade-left-leave-to {
  opacity: 0;
}
</style>
