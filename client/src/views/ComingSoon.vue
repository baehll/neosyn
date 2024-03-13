<template>
  <div class="coming-soon">
    <video src="/assets/videos/coming-soon.mp4"
           autoplay
           loop
           muted
    />
    <div class="wrap pt-20 px-20 pb-16">
      <div class="flex flex-col h-full justify-between">
        <Logo class="text-primary logo"/>
        <div class="flex flex-col justify-between">
          <h1 class="font-mondwest mb-64" v-text="$i18n.t('coming soon')"></h1>
          <div class="flex flex-row justify-between items-center">
            <p class="font-nimbus" v-html="translation.instagram"></p>
            <ul class="flex flex-row gap-6 text-lightgray-10">
              <li><a @click="toggleLogin" v-text="$t('Login')"></a></li>
              <li>
                <router-link to="/privacy-policy" v-text="$t('Privacy Policy')"></router-link>
              </li>
              <li>
                <router-link to="/imprint" v-text="$t('Imprint')"></router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <LoginLayer
      :login-visible="loginVisible"
      @hide="loginVisible = false"
    />
  </div>
</template>
<script>

import Logo from '../components/global/logo.vue';
import Instagram from '../components/global/instagram.vue';
import LoginLayer from '../components/LoginLayer.vue';
import login from './Login.vue';

export default {
  name: 'ComingSoon',
  components: {LoginLayer, Instagram, Logo},
  data: function() {
    return {
      translation: {
        instagram: this.$t('Follow us on <a href="https://www.instagram.com/neosyn.ai" class="underline">Instagram</a> for the latest updates.')
      },
      loginVisible: false,
    }
  },
  computed: {
    login() {
      return login
    }
  },
  methods: {
    toggleLogin() {
      this.loginVisible = !this.loginVisible;
    }
  },
  created: () => {

  }
}
</script>

<style lang="scss" scoped>
.coming-soon {
  @apply relative;
  height: 100dvh;
  width: 100dvw;

  h1 {
    font-weight: 100;
    font-size: 8.75rem !important;
  }

  .logo {
    width: 99px;
    height: 61px;
  }
}


p {
  font-size: 1.5rem !important;
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