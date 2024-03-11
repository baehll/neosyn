<template>
  <div class="coming-soon">
    <video src="/assets/videos/coming-soon.mp4"
           autoplay
           loop
           muted
    />
    <div class="wrap pt-20 px-20 pb-16">
      <div class="flex flex-col h-full justify-between">
        <Logo/>
        <div class="flex flex-col justify-between">
          <h1 class="font-mondwest mb-64">coming soon</h1>
          <div class="flex flex-row justify-between items-center">
            <p class="font-nimbus">Follow us on <a href="#" class="underline">Instagram</a> for the latest updates.</p>
            <ul class="flex flex-row gap-6 text-lightgray-10">
              <li><a href="#login">Login</a></li>
              <li><a href="#privacy">Privacy Policy</a></li>
              <li><a href="#imprint">Imprint</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import Logo from '../components/global/logo.vue';
import Instagram from '../components/global/instagram.vue';

export default {
  name: 'ComingSoon',
  components: {Instagram, Logo},
  data: () => {
    return {}
  },
  computed: {},
  methods: {},
  created: () => {

  }
}
</script>

<style lang="scss">
.coming-soon {
  @apply relative;
  height: 100dvh;
  width: 100dvw;
}

h1 {
  font-weight: 100;
  font-size: 8.75rem !important;
}

p {
  font-size: 1.5rem !important;
}

svg {
  width: 99px;
  height: 61px;

  path {
    fill: #ACED84;
  }
}

video {
  width: 100%;
  height: 100% !important;
  max-width: none !important;
  object-fit: cover;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
}

.wrap {
  position: absolute;
  width: 100%;
  height: 100%;
  color: #ACED84;
  @apply top-0 left-0;

}
</style>