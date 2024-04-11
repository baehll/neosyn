<template>
	<div :class="{'cursor-pointer mb-3 gap-2 flex items-center': true, 'text-lightgray-40': disabled, 'flex-row justify-end': rtl, 'justify-end flex-row-reverse': !rtl}">
		<label :for="id" v-text="label"></label>
		<input 
			:id="id"
			:disabled="disabled" 
			type="checkbox" 
			:value="id" 
			@change="update" 
			:checked="modelValue && modelValue.indexOf(id) !== -1" 
			:class="{'w-4 transition-colors h-4 appearance-none rounded-full border bg-transparent checked:bg-primary': true, 'border-lightgray-80': !disabled, 'border-lightgray-40': disabled}"
			>
	</div>
</template>
<script>
export default {
	name: 'Checkbox',
	props: ['id','modelValue','label','rtl', 'disabled'],
	computed: {
	},
	methods:{
		update($event){
			let updatedSelection = []
			if ($event.target.checked) {
        updatedSelection = this.modelValue.concat(this.id);
      } else {
        updatedSelection = this.modelValue.filter(x => x !== this.id);
      }
			this.$emit('update:modelValue', updatedSelection)
		}
	},
	created(){
console.log(this.modelValue)
	}
}
</script>
<style lang="scss">
label {
	@apply text-sm;
}
	
</style>
