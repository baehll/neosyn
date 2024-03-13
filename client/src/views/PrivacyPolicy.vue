<template>
  <MetaPage
    title="privacy policy"
  >
<template v-slot:navigation>
  <li><router-link to="/">Home</router-link></li>
  <li><router-link to="/imprint">Imprint</router-link></li>
</template>
  </MetaPage>
</template>
<script>

import MetaPage from '../components/global/MetaPage.vue';

export default {
  name: 'Privacy Policy',
  components: {MetaPage},
  emits: [],
  props: {},
  data: () => {
    return {}
  },
  computed: {},
  methods: {},
  mounted: function () {

  },
  created: function () {

  }
}
</script>

<style lang="scss" scoped>

</style>