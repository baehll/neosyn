<template>
  <div class="h-full">
  <component
    :is="currentStepComponent"
  />
  </div>
</template>
<script>

import ProgressBar from '../components/global/ProgressBar.vue';
import Step1 from '../components/registration/Step1.vue';
import Button from '../components/global/Button.vue';

export default {
  name: 'Registration',
  components: {
    Button,
    ProgressBar
  },
  data: () => {
    return {
      currentStepComponent: Step1,
      currentStep: 1
    }
  },
  computed: {},
  methods: {
    nextStep() {
      console.log("next");
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">
</style>


