<template>
  <div class="coming-soon">
    <video src="/assets/videos/coming-soon.mp4"
           autoplay
           loop
           muted
    />
    <div class="wrap">
      <div class="flex flex-col h-full justify-between">
        <div class="flex justify-between">
          <logo-big class="text-primary logo"/>
          <ul class="lg:hidden flex flex-row gap-6 text-lightgray-10">
            <li>
              <router-link to="/privacy-policy" v-text="$t('Privacy Policy')"></router-link>
            </li>
            <li>
              <router-link to="/imprint" v-text="$t('Imprint')"></router-link>
            </li>
          </ul>
        </div>
        <div class="flex flex-col justify-between">
          <h1 class="font-mondwest mt-64 mb-36 lg:mt-0 lg:mb-80" v-text="$i18n.t('coming soon')"></h1>
          <div class="flex flex-row justify-between items-center">
            <p class="hidden lg:block font-nimbus" v-html="translation.instagram"></p>
            <ul class="hidden lg:flex flex-row gap-6 text-lightgray-10">
              <li><a class="cursor-pointer" @click="toggleLogin" v-text="$t('Login')"></a></li>
              <li>
                <router-link to="/privacy-policy" v-text="$t('Privacy Policy')"></router-link>
              </li>
              <li>
                <router-link to="/imprint" v-text="$t('Imprint')"></router-link>
              </li>
            </ul>
            <a class="lg:hidden" href="https://www.instagram.com/neosyn.ai" target="_blank">
              <instagram-outline
                class="mb-52"

              />
            </a>
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
import LogoBig from '../components/global/logo-big.vue';
import InstagramOutline from '../components/global/instagram-outline.vue';

export default {
  name: 'ComingSoon',
  components: {InstagramOutline, LogoBig, LoginLayer, Instagram, Logo},
  data: function () {
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
  height: 100%;
  width: 100%;

  h1 {
    font-weight: 100;
    font-size: calc(60rem / 16);
    line-height: 1.2;
    max-width: 75%;

    @screen md {
      font-size: 6.75rem !important;
      max-width: none;
    }
  }

  .logo {
    width: 52px;
    height: 32px;
    @screen md {
      width: 99px;
      height: 61px;
    }
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
  @apply pt-8 px-6;
  @screen md {
    @apply pt-20 px-20 pb-16;
  }
  position: absolute;
  width: 100%;
  height: 100%;
  color: #ACED84;
  @apply top-0 left-0;

}
</style>
