<template>
  <nav class="h-full pt-4 pb-6 px-3 bg-darkgray-20 border-r border-l border-lightgray-70 sidebar flex flex-col">
    <logo-big
      class="shrink-0 mb-16 self-end text-white logo-sidebar"
    />
    <div class="flex flex-col justify-between h-full">
      <ul class="flex flex-col items-center gap-12 text-lightgray-10">
        <li>
          <router-link to="inbox"><inbox
         :class="{'text-primary': $route.name === 'Inbox'}"
          /></router-link>
        </li>
        <li>
          <router-link to="notifications"><notifications/></router-link>
        </li>
        <li>
          <router-link to="analytics"><analytics/></router-link>
        </li>
        <li class="separator"></li>
        <li>
          <router-link to="audience"><audience/></router-link>
        </li>
        <li>
          <router-link to="bookmarks"><bookmarks/></router-link>
        </li>
      </ul>
      <ul class="mb-4 flex flex-col items-center gap-10 text-lightgray-10">
        <li class="separator"></li>
        <li>🙆‍♂️</li>
        <li><settings/></li>
      </ul>
    </div>
  </nav>

</template>
<script>
import Logo from '../global/logo.vue';
import Inbox from '../global/inbox.vue';
import Notifications from '../global/notifications.vue';
import Analytics from '../global/analytics.vue';
import Audience from '../global/audience.vue';
import Bookmarks from '../global/bookmarks.vue';
import Settings from '../global/settings.vue';
import LogoBig from '../global/logo-big.vue';

export default {
  name: 'SidebarNavigation',

  components: {LogoBig, Settings, Bookmarks, Audience, Analytics, Notifications, Inbox, Logo},
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
.separator {
  height: 1px;
  width: 100%;
  @apply bg-lightgray-10;
}
.logo-sidebar {
  width: 40px;
}
.sidebar {
  width: 70px;
}

</style>
