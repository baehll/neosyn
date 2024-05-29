<template>
  <div class="pt-7 flex flex-col justify-between relative bg-darkgray">
    <div class="px-3 relative w-full mb-4">
      <Searchglass
        class="text-lightgray-10 absolute left-6 top-1/2 transform -translate-y-1/2 pointer-events-none"
      />
      <input type="text" class="bg-transparent border border-lightgray-10 py-0 px-24 w-full"
        v-model="searchTerm"
        @keyup.enter="commitSearch"
      >
    </div>
    <div class="px-3 justify-between relative flex flex-row">
      <div class="flex items-center gap-2 w-8/1 pt-3 pb-4">
        <Reload
          class="text-lightgray-10"
          @click="fetchThreads"
        />
        <TimeDifferenceDisplay
          :point-in-time="threadStore.lastUpdated"
          class="text-lightgray-10 text-sm"
        />
      </div>
      <div class="flex gap-2">
        <CustomButton
          @click="toggleFilterLayer"
            :class="{'!pb-4 relative top-0.5 z-50 icon-only !px-2 !pt-3 block border !rounded-none': true, 'border-transparent': !filterLayerVisible, '!bg-black border-lightgray-80 border-b-black': filterLayerVisible}"
        >
          <span
          >
          <Filter
          />
          </span>
        </CustomButton>
        <CustomButton
          @click="toggleSorting"
            :class="{'!pb-4 relative top-0.5 z-50 icon-only !px-2 !pt-3 block border !rounded-none': true, 'border-transparent': !sortingLayerVisible, '!bg-black border-lightgray-80 border-b-black': sortingLayerVisible}"
        >
          <span
          >
          <Sorting/>
          </span>
        </CustomButton>
      </div>
    </div>
    <div class="flex flex-col">
      <div v-if="sortingLayerVisible" class="flex flex-col w-full border-t border-lightgray bg-black text-white px-6 pt-3 pb-4 relative justify-between">
        <small v-text="$t('Sort by:')" class="text-lightgray-10 font-roboto mb-2"></small>
        <ul
          :class="{'flex flex-wrap': true}"
        >
          <li
            v-for="(sortingTitle, sortingOption) in sortingOptions"
            :key="sortingOption"
            :class="{'basis-1/2 mb-2 text-sm even:text-right': true}"
          >
            <button
              v-text="sortingTitle"
              :class="{'font-roboto hover:font-medium': true, 'text-primary font-medium': sortingOption === sorting, 'text-white': sortingOption !== sorting}"
              @click="setSorting(sortingOption)"
            ></button>
          </li>
        </ul>
      </div>
      <div v-if="filterLayerVisible" class="flex flex-row w-full bg-black text-white px-6 py-4 border-t border-lightgray relative justify-between">
        <ul>
          <li
            v-for="(platform) in availableFilters.platforms"
            :key="platform.name"
          >
            <Checkbox
              :label="platform.name"
              :id="platform.id"
              :disabled="platform.is_implemented === false"
              v-model="platformFilter"
              @value-changed="filterChanged"
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
              @value-changed="filterChanged"
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
import {usePlatformStore} from '../../stores/platforms.js'

export default {
  name: 'ThreadTopBar',
  emits: ['triggered-search', 'changed-filter', 'changed-sorting'],
  components: {TimeDifferenceDisplay, Reload, Searchglass, Sorting, Filter, CustomButton, Checkbox},
  data: () => {
    return {
      filterLayerVisible: false,
      sortingLayerVisible: false,
      searchTerm: '',
      threadFilter: null,
      sorting: 'desc',
      messageTypeFilter: [],
      platformFilter: [],
    }
  },
  computed: {
    ...mapStores(useThreadStore, usePlatformStore),
    sortingOptions() {
      return {
           'new': this.$t('New'),
           'old': this.$t('Old'),
           'most_interaction': this.$t('Most Interaction'),
           'least_interaction': this.$t('Least Interaction'), 
        }
    },
    availableFilters() {
      const result = {}
      result.platforms = this.platformStore.platforms
      result.messageTypes = ThreadFilter.MESSAGE_TYPES
      return result
    },
  },
  methods: {
    setSorting(sorting){
      this.sorting = sorting
      this.$emit('changed-sorting', this.sorting)
    },
    filterChanged(){
      this.$emit('changed-filter', {
        platform: this.platformFilter,
        sentiment: this.messageTypeFilter
      })
    },
    commitSearch() {
      this.$emit('triggered-search', this.searchTerm)
    },
    toggleFilterLayer() {
      this.sortingLayerVisible = false
      this.filterLayerVisible = !this.filterLayerVisible
    },
    toggleSorting() {
      this.filterLayerVisible = false
      this.sortingLayerVisible = !this.sortingLayerVisible
    }
  },
  async created() {
    this.threadFilter = new ThreadFilter
    await this.platformStore.getPlatforms()
  }
}
</script>

<style lang="scss" scoped>
input {
  &[type="text"] {
    @apply py-1.5 px-10 outline-0 bg-transparent focus:border-primary hover:bg-lightgray;
    border-radius: 36px;
  }
}
</style>
