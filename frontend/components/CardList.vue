<template>
  <div class="flex flex-wrap p-10 justify-center">
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
  </div>
</template>

<script setup>
import { fetchRecipes } from '@/services/fetchs'
const { data: recipies } = await fetchRecipes()
</script>
