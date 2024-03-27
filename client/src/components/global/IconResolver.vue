<template>
  <component :is="iconComponent"/>
</template>
<script>

export default {
  name: 'IconResolver',
  emits: [],
  props: ['iconName'],
  computed: {
    iconComponent() {
      // Dynamically import the icon component based on the iconName prop
      return import('./' + this.iconName.charAt(0).toUpperCase() + this.iconName.slice(1) + '.vue')
        .then(res => res.data)
        .catch(err => {
          console.error('Icon not found: ', this.iconName);
          return Promise.resolve({template: '<span>Icon not found</span>'});
        })
    },
  },
}
</script>

<style lang="scss" scoped>

</style>