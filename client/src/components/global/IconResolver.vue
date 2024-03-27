<template>
  <component :is="iconComponent"/>
</template>
<script>

import Instagram from './instagram.vue';
import Facebook from './facebook.vue';
import X from './x.vue';
import Linkedin from './linkedin.vue';

export default {
  name: 'IconResolver',
  emits: [],
  props: ['iconName'],
  computed: {
    iconComponent() {
      let icon = ''
      switch (this.iconName) {
        case 'instagram':
          icon = Instagram
          break;
        case 'facebook':
          icon = Facebook
              break;
        case 'twitter':
        case 'x':
          icon = X
              break;
        case 'linkedin':
          icon = Linkedin
              break;
      }
      return icon
    },
  },
}
</script>

<style lang="scss" scoped>

</style>