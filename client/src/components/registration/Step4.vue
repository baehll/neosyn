<template>
  <div>
    <h2 v-text="$t('Welcome :name').replace(':name', userStore.name)"></h2>
    <p v-text="$t('This is your new membercard.')"></p>
  </div>
</template>
<script>

import Button from '../global/CustomButton.vue';
import IdCard from '../IdCard.vue';
import {useUserStore} from '../../stores/user.js';
import {mapStores} from 'pinia';

export default {
  emits: ['nextStep', 'prevStep'],
  name: 'Registration Step 1',
  components: {IdCard, Button},
  data: () => {
    return {}
  },
  computed: {
     ...mapStores(useUserStore)
  },
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