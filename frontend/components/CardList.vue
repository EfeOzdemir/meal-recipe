<template>
  <div class="flex flex-wrap p-10 gap-x-4 gap-y-8 m-auto max-w-[1400px]">
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
  </div>
</template>

<script setup>
const { data: recipies, pending, error, refresh } = await useAsyncData(
  'recipie',
  () => $fetch("http://localhost:5000/recipe/")
)
</script>
