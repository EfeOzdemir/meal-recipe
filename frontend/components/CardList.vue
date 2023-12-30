<template>
  <div v-for="recipe in recipies" :key="recipe.id">
    <Card :recipe="recipe" />
  </div>
</template>

<script setup>
const recipies = ref([]);
const getRecipies = async () => {
  const { data, error } = await useMyFetch("/recipe", {
    method: "get",
  });

  if (data) {
    recipies.value = data.value;
  }
};
getRecipies();
</script>

<style lang="scss" scoped></style>
