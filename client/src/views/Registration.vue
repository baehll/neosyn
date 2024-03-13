<template>
  <div class="flex flex-row h-full">
    <div class="flex flex-col justify-between basis-1/3 bg-darkgray p-8 text-white">
      <div>
        <Button
          :class="{'icon-only transition-opacity': true, 'opacity-0 invisible': currentStep === 0, 'opacity-100': currentStep > 0}"
          @click="previousStep"
        >
          <chevron-left
            class=""
          />
        </Button>

        <transition name="fade-left" mode="out-in">
          <component
            :key="currentStep"
            v-if="currentStepComponent"
            :is="currentStepComponent"
            @turned-valid="turnStepValid"
            @turned-invalid="turnStepInvalid"
          />
        </transition>
      </div>
      <div class="flex flex-row justify-between items-center">
        <ProgressBar
          class="basis-1/4"
          :percentage="(currentStep+1)/((steps.length)/100)"
        />
        <Button
          class="basis-1/4 bg-lightgray-60 text-darkgray"
          v-if="currentStep < steps.length - 1"
          @click="nextStep"
        >
          {{ $t('Continue') }}
        </Button>
      </div>
    </div>

    <div class="basis-2/3 bg-lightgray flex items-center justify-center">
      <IdCard/>
    </div>
  </div>
</template>
<script>

import ProgressBar from '../components/global/ProgressBar.vue';
import Step1 from '../components/registration/Step1.vue';
import Button from '../components/global/Button.vue';
import IdCard from '../components/IdCard.vue';
import Step2 from '../components/registration/Step2.vue';
import ChevronLeft from '../components/global/chevron-left.vue';
import Step3 from '../components/registration/Step3.vue';

export default {
  name: 'Registration',
  components: {
    ChevronLeft,
    IdCard,
    Button,
    ProgressBar
  },
  data: () => {
    return {
      steps: [
        Step1,
        Step2,
        Step3
      ],
      validSteps:{},
      currentStepComponent: Step1,
      currentStep: 0
    }
  },
  computed: {},
  methods: {
    nextStep() {
      if (this.currentStep === this.steps.length - 1) {
        return
      }
      this.currentStep++;
      this.currentStepComponent = this.steps[this.currentStep];
    },
    previousStep() {
      if (this.currentStep === 0) {
        return
      }
      this.currentStep--;
      this.currentStepComponent = this.steps[this.currentStep];
    },
    turnStepValid() {
      this.validSteps[this.currentStep] = true
    },
    turnStepInvalid() {
      this.validSteps[this.currentStep] = false
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
.fade-left-enter-active,
.fade-left-leave-active {
  transition: opacity 0.5s ease;
}

.fade-left-enter-from,
.fade-left-leave-to {
  opacity: 0;
}
</style>


