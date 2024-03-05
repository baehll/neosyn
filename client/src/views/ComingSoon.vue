<template>
<Logo/>
  <instagram/>
  <a href="#">Login</a>
  <div>
    <video src="/assets/videos/coming-soon.mp4"
      autoplay
      loop
      muted
    />
    <div class="wrap">
      <h1>Coming Soon</h1>
      <p>Follow us on Instagram for the latest updates.</p>
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
    return {

    }
  },
  computed: {

  },
  methods: {

  },
  created: () => {

  }
}
</script>

<style lang="scss" scoped>
svg {
  path {
    fill: #ACED84;
  }
}
video {
  width: 100dvw;
  height: 100dvh;
  object-fit: cover;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
}

.wrap {
  position: absolute;
  bottom: 10%;
  left: 5%;

  color: #ACED84;
  font-family: "PP NeueBit";
  font-size: 80px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
}
</style>