<template>
    <div class="shrink-0 message-post-wrap overflow-hidden h-full py-5 bg-lightgray pr-5">
      <div class="overflow-hidden flex flex-col justify-between w-full h-full rounded-xl message gap-4">
        <MessagePost

      />
        <MessageInsights

      />
      </div>
    </div>
</template>
<script>
import MessageInsights from './MessageInsights.vue';
import MessagePost from './MessagePost.vue';


export default {
	name: 'PostContainer',
	components: {
		MessagePost,
		MessageInsights,
	}
}
</script>
<style lang="scss">
.message-post-wrap {
	width: 216px;

	@media (min-width: 1920px) {
		width: 405px;
	}
}
</style>
