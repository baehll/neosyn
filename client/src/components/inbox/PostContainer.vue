<template>
    <div class="shrink-0 message-post-wrap overflow-hidden h-full py-5 bg-lightgray">
      <div class="overflow-hidden flex flex-col justify-between w-full h-full rounded-xl message gap-4">
				<MessagePost
					:message-post="messagePost"
					:likes="messagePost?.likes"
					:shares="messagePost?.shares"
					:comments="messagePost?.comments"
					:image="messagePost?.postMedia"
					:content="messagePost?.postContent"
				/>
				<MessageInsights

				/>
      </div>
    </div>
</template>
<script>
import { mapStores } from 'pinia';
import MessageInsights from './MessageInsights.vue';
import MessagePost from './MessagePost.vue';
import {useMessagePostStore} from '../../stores/messagepost.js'

export default {
	name: 'PostContainer',
	components: {
		MessagePost,
		MessageInsights,
	},
	props: {
		threadId: {
			type: Number
		},
	},
	data: () => {
		return {
			messagePost: null,
		}
	},
	computed: {
		...mapStores(useMessagePostStore),
	},
  watch: {
    async threadId(newVal, oldVal) {
      this.messagePost = await this.messagePostStore.getPostForThread(newVal)
    }
  },
}
</script>
<style lang="scss">
.message-post-wrap {
	width: 216px;

	@media (min-width: 1650px) {
		width: 405px;
	}
	@media (max-width: 1300px) {
		@apply hidden;
	}
}
</style>
