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
          <Button class="ghost" @click="nextStep" v-if="steps[currentStep].hasSkipOption">
            {{ $t('Skip') }}
          </Button>
          <Button class="basis-1/4 bg-lightgray-60 text-darkgray" :disabled="!isValid"
                  v-if="currentStep < steps.length - 1" @click="nextStep">
            {{ $t('Continue') }}
          </Button>
          <Button class="basis-1/4" v-if="currentStep === steps.length - 1" @click="finishRegistration">
            {{ $t('Continue') }}
          </Button>
        </div>
      </div>
    </div>

    <div class="relative basis-2/3 bg-lightgray flex items-center justify-center">
      <div class="absolute w-full h-full top-0 left-0">

      </div>
      <IdCard />
    </div>
    <Logo class="absolute top-8 right-8 w-6 header-left text-lightgray-10" />
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

export default {
  name: 'Registration',
  components: {
    Logo,
    ChevronLeft,
    IdCard,
    Button,
    ProgressBar
  },
  data: () => {
    return {
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
          validation: () => {
            return true
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
    nextStep() {
      if (this.currentStep === this.steps.length - 1) {
        return
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
    finishRegistration() {
      this.$router.push('company-info')
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
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
    @apply border border-lightgray focus:border-primary ring-0 focus:outline-0 outline-0 focus:ring-0 focus:ring-offset-0 rounded-lg w-full bg-transparent;
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