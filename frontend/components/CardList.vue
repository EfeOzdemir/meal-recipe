<template>
  <CardFilter />
  <div class="flex flex-wrap p-10 gap-x-4 gap-y-8 m-auto max-w-[1400px]">
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
  </div>
</template>

<script setup>
const { data } = await useAsyncData("recipe", () =>
  $fetch("http://127.0.0.1:5000/recipe/")
);
const recipies = data;
</script>
