<template>
	<div class="h-full text-center">
		<div class="hover-trigger relative flex flex-col gap-2 items-center p-6 border border-lightgray rounded-lg hover:border-primary cursor-pointer ">
			<button
				class="hidden absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 rounded-full bg-primary p-2 text-black"
				@click.stop.prevent="deleteFile"
				>
				<close/>
			</button>
			<component
			:is="filetypeLogo"
			class="w-12 h-12"
			/>
		</div>
		<small class="mx-auto w-10/12 overflow-hidden text-xs mt-1 block overflow-ellipsis whitespace-nowrap">
			{{filename}}
		</small>
	</div>
</template>
<script>
import pdf from '../global/pdf.vue'
import csv from '../global/csv.vue'
import docx from '../global/docx.vue'
import html from '../global/html.vue'
import json from '../global/json.vue'
import tex from '../global/tex.vue'
import txt from '../global/txt.vue'
import pptx from '../global/pptx.vue'
import md from '../global/md.vue'
import close from '../global/close.vue'

export default {
	name: 'UploadedFile',
	emits: ['deleteFile'],
	components: {
		pdf,
		csv,
		docx,
		html,
		json,
		tex,
		txt,
		pptx,
		md,
		close,
	},
	props: {
		filename: {
			type: String
		}
	},
	data: () => {
		return {

		}
	},
	computed: {
		filetypeLogo(){
			return this.filename.split('.').pop()
		}
	},
	methods: {
		deleteFile(){
			this.$emit('deleteFile', this.filename)
		}
	},
	created(){

	}
}
</script>
<style lang="scss" scoped>
.hover-trigger {
	&:hover {
		button {
			@apply block;
		}
	}
}
</style>
