<template>
  <div class="flex flex-row h-full">
    <div class="basis-1/3 bg-darkgray p-8">
      <Button
        @click="nextStep"
        :cta="$t('Next')"
      />
    </div>
    <div class="basis-2/3 bg-lightgray flex items-center justify-center">
      <IdCard/>
    </div>
  </div>

</template>
<script>

import Button from '../global/Button.vue';
import IdCard from '../IdCard.vue';

export default {
  emits: ['nextStep', 'prevStep'],
  name: 'Registration Step 1',
  components: {IdCard, Button},
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