<template>
  <div>
    Step 3
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