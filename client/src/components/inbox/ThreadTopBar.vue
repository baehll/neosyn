<template>
  <div class="pt-7 pb-5 flex flex-col justify-between relative bg-darkgray-10">
    <div class="px-3 relative w-full mb-8">
      <Searchglass
        class="text-lightgray-10 absolute left-6 top-1/2 transform -translate-y-1/2 pointer-events-none"
      />
      <input type="text" class="bg-transparent border border-lightgray-10 py-0 px-24 w-full"
             @keyup.enter="commitSearch">
    </div>
    <div class="px-3 justify-between relative flex flex-row">
      <div class="flex items-center gap-2 w-8/12">
        <Reload
          class="text-lightgray-10"
        />
        <TimeDifferenceDisplay
          :point-in-time="threadStore.lastUpdated"
          class="text-lightgray-10 text-sm"
        />
      </div>
      <div class="flex gap-2">
        <CustomButton
          :class="{'icon-only': true}"
          @click="toggleFilterLayer"
        >
          <span
            :class="{'px-2 pt-1 block': true, 'bg-lightgray border border-lightgray-20': filterLayerVisible}"
          >
          <Filter
          />
          </span>
        </CustomButton>
        <CustomButton
          class="icon-only"
          @click="toggleSorting"
        >
          <Sorting/>
        </CustomButton>
      </div>
    </div>
    <div class="flex flex-col">
      <div v-if="sortingLayerVisible" class="bg-primary px-6 py-4 absolute left-0 top-full">
        <ul>
          <li
            v-for="(label, icon) in availableFilters.platforms"
            :key="icon"
          >
            <input type="checkbox" :name="`${icon}-filter`" :id=" `${icon}-filter`">
            <label :for="`${icon}-filter`">
              <span v-text="label"></span>
            </label>
          </li>
        </ul>
      </div>
      <div v-if="filterLayerVisible" class="flex flex-row w-full bg-darkgray text-white px-6 py-4 relative justify-between">
        <ul>
          <li
            v-for="(platform) in availableFilters.platforms"
            :key="platform.name"
          >
            <Checkbox
              :label="platform.label"
              :id="platform.name"
              :disabled="platform.disabled && platform.disabled === true"
              v-model="platformFilter"
            />
          </li>
        </ul>
        <ul>
          <li
            v-for="messageType in availableFilters.messageTypes"
          >
            <Checkbox
              :rtl="true"
              :label="messageType.label"
              :id="messageType.name"
             v-model="messageTypeFilter"
            />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
import Checkbox from '../global/checkbox.vue';
import ThreadFilter from '../../lib/ThreadFilter.js';
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
  components: {TimeDifferenceDisplay, Reload, Searchglass, Sorting, Filter, CustomButton, Checkbox},
  data: () => {
    return {
      filterLayerVisible: false,
      searchTerm: '',
      threadFilter: null,
      sorting: 'desc',
      messageTypeFilter: [],
      platformFilter: [],
    }
  },
  computed: {
    ...mapStores(useThreadStore),
    availableFilters() {
      const result = {}
      result.platforms = ThreadFilter.AVAILABLE_PLATFORMS
      result.messageTypes = ThreadFilter.MESSAGE_TYPES
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
input {
  &[type="text"] {
    @apply py-1.5 px-10 rounded-xl outline-0 bg-transparent;
  }
}
</style>
