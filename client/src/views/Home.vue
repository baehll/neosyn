<template>
  <div class="container">
    <div class="grid">
      <div class="col-span-6">
        <div class="p-4">
          <ProgressBar
            :percentage="progress"
          />
          <button @click="increaseProgress">Increase</button>
        </div>
      </div>
    </div>

  </div>
</template>
<script>

import ProgressBar from '../components/global/ProgressBar.vue';

export default {
  name: 'Home',
  components: {ProgressBar},
  data: () => {
    return {
      progress: 10,
      percentage: 100,
    }


  },
  computed: {},
  methods: {
    increaseProgress() {
      this.progress += 10;
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss">

</style>