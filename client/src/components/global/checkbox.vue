<template>
	<div class="flex gap-2 items-center">
	<label :for="id" v-text="label" v-if="rtl"></label>
	<input type="checkbox" :value="id" @change="update" :checked="modelValue && modelValue.indexOf(id) !== -1" class="w-4 transition-colors h-4 appearance-none rounded-full border border-primary bg-transparent checked:bg-primary">
	<label :for="id" v-text="label" v-if="!rtl"></label>
	</div>
</template>
<script>
export default {
	name: 'Checkbox',
	props: ['id','modelValue','label','rtl'],
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
