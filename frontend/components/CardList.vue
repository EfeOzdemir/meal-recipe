<template>
  <div class="flex flex-wrap p-10 gap-x-4 gap-y-8 m-auto w-[1600px]">
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
  </div>
</template>

<script setup>
import { fetchRecipes } from "@/services/fetchs";
const { data: recipies } = await fetchRecipes();

</script>
