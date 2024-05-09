<template>
	<div class="w-full h-full flex flex-col justify-end items-center">
		<div class="w-8/12 rounded-lg bg-darkgray border border-lightgray mb-24">
			<div class="text-white border-b border-lightgray p-4" v-text="getApostrophedName + ' ' + $t('Documents') "></div>
			<div class="h-64"></div>
		</div>
		<div class="progressbar w-8/12 h-2 mb-2 bg-primary rounded-lg"></div>
		<div class="mb-16 text-white">Upload progress</div>
	</div>
</template>
<script>
import { mapStores } from 'pinia';
import { useUserStore } from '../../stores/user';


export default {
	name: 'UploadProgressIndicator',
  emits: [],
  props: {
		uploadStarted: {
			type: Boolean
		}
  },
  data: () => {
    return {

    }
  },
  computed: {
		...mapStores(useUserStore),
		getApostrophedName(){
			const lastChar = this.userStore.name.charAt(this.userStore.name.length - 1)
			return lastChar.toLowerCase() === 's' ?
				`${this.userStore.name}'` :
				`${this.userStore.name}'s`
		}
  },
  methods: {

  },
  mounted: function() {
  },
  created: function() {

  }
}
</script>
<style lang="scss" scoped>

</style>

