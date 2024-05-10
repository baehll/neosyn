<template>
	<div class="w-full h-full flex flex-col justify-center  items-center">
		<div class="w-8/12 rounded-lg bg-darkgray border border-lightgray mb-24">
			<div class="text-white border-b border-lightgray p-4" v-text="getApostrophedName + ' ' + $t('Documents') "></div>
			<div class="h-80 bt-24 mb-48 flex justify-center items-center">
				<highlightedfile
				class="custom-fill"
					v-if="userStore.companyFiles.length"
				/>
			</div>
		</div>
		<div :class="{'w-full flex flex-col items-center': true, 'invisible': !uploadStarted}">
			<div class="progressbar w-8/12 h-2 mb-2 bg-lightgray overflow-hidden rounded-lg"></div>
			<div class="mb-16 text-white">Upload progress</div>
		</div>
	</div>
</template>
<script>
import { mapStores } from 'pinia';
import { useUserStore } from '../../stores/user';
import highlightedfile from '../global/highlighted-file.vue'

export default {
	name: 'UploadProgressIndicator',
  emits: [],
	components: {
		highlightedfile
	},
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
.progressbar {
	@apply relative;

	&:before {
		content: '';
		@apply absolute left-0 top-0 w-0 h-full bg-primary rounded-lg;
	}

&.uploading {
		&:before {
			animation: bar 4s infinite;
		}
	}

	@keyframes bar {
		0% {
			width: 0;
		}
		35% {
			width: 25%;
		}
		50% {
			width: 45%;
		}
		90% {
			width: 100%;
		}
		100% {
			width: 100%;
		}
	}
}
</style>

