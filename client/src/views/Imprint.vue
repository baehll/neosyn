<template>
  <MetaPage
    title="imprint">
    <template v-slot:navigation>
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/privacy-policy">Privacy Policy</router-link>
      </li>
    </template>
    <template v-slot:content>
      <div class="flex text-white px-12 mt-16 items-end">
        <div class="basis-8/12">
          <p>
            Impressum<br>
            Pflichtangaben für Diensteanbieter gem. §5 Telemediengesetz (TMG)<br>
            neosyn GmbH<br>
          </p>
          <p>
            Handelsregister <br>
            HRB 41830 | Amtsgericht Leipzig<br>
            Umsatzsteueridentifikationsnummer (USt-Id)<br>
            DE357174914<br>
          </p>
          <p>
            Geschäftsführer<br>
            Maximilian Schöne<br>
            <br>
            Sitz der Gesellschaft<br><br>
            Lützner Str. 84<br>
            04177 Leipzig<br>
          </p>
        </div>
        <div class="basis-4/12">
          <p>
            Telefon<br>
            <a href="tel:+4915114378797">+49 (0)151 14378797</a><br><br>

            E-Mail<br>
            <a href="mailto:info@neosyn.ai">info@neosyn.ai</a>
          </p>
        </div>
      </div>
    </template>
  </MetaPage>
</template>
<script>

import MetaPage from '../components/global/MetaPage.vue';

export default {
  name: 'Imprint',
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
p {
  @apply mb-12;
}

</style>