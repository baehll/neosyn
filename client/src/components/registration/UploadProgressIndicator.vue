<template>
	<div>
		<span v-text="userStore.name"></span>
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

