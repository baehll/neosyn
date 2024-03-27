<template>
  <div class="flex flex-col justify-between relative">
    <div class="relative w-8/12 mb-4">
      <Searchglass
        class="text-lightgray-10 absolute left-4 top-1/2 transform -translate-y-1/2 pointer-events-none"
      />
      <input type="text" class="border border-lightgray-10 py-0 px-4 w-full" @keyup.enter="commitSearch">
    </div>
    <div class="justify-between relative flex flex-row">
      <div class="flex items-center gap-2 w-8/12">
        <Reload
          class="text-lightgray-10"
        />
        <TimeDifferenceDisplay
          :point-in-time="threadStore.lastUpdated"
          class="text-lightgray-10"
        />
      </div>
      <div class="flex gap-2">
        <CustomButton
          class="icon-only"
          @click="toggleFilterLayer"
        >
          <Filter/>
        </CustomButton>
        <CustomButton
          class="icon-only"
          @click="toggleSorting"
        >
          <Sorting/>
        </CustomButton>
      </div>
      <div v-if="filterLayerVisible" class="bg-primary px-8 py-4 -32 -32 absolute left-0 top-full">
        Show only selected social media networks
        <ul>
          <li
            v-for="(label, icon) in availableFilters.platforms"
            :key="icon"
          >
            <input type="checkbox" :name="`${icon}-filter`" :id=" `${icon}-filter`">
            <label :for="`${icon}-filter`">
              <span v-text="label"></span>
              <component :is="icon"></component>
            </label>
          </li>
        </ul>

      </div>
    </div>
  </div>
</template>
<script>

import ThreadFilter from '../../lib/threadFilter.js';
import CustomButton from '../global/CustomButton.vue';
import Filter from '../global/filter.vue';
import Sorting from '../global/sorting.vue';
import Searchglass from '../global/searchglass.vue';
import Reload from '../global/reload.vue';
import {mapStores} from 'pinia';
import {useThreadStore} from '../../stores/thread.js';
import TimeDifferenceDisplay from '../global/TimeDifferenceDisplay.vue';

export default {
  name: 'ThreadTopBar',
  components: {TimeDifferenceDisplay, Reload, Searchglass, Sorting, Filter, CustomButton},
  data: () => {
    return {
      filterLayerVisible: false,
      searchTerm: '',
      threadFilter: null,
      sorting: 'desc'
    }
  },
  computed: {
    ...mapStores(useThreadStore),
    availableFilters() {
      const result = {}
      result.platforms = ThreadFilter.AVAILABLE_PLATFORMS
      return result
    }

  },
  methods: {
    commitSearch() {
    },
    toggleFilterLayer() {
      this.filterLayerVisible = !this.filterLayerVisible
    },
    toggleSorting() {
    }
  },
  created() {
    this.threadFilter = new ThreadFilter
  }
}
</script>

<style lang="scss">

</style>