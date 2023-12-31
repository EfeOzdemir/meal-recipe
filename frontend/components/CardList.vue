<template>
  <div class="flex flex-wrap p-10 gap-x-4 gap-y-8 m-auto max-w-[1400px]">
    <Card v-for="recipe in recipies" :id="recipe.id" :recipe="recipe" />
  </div>
</template>

<script setup>
const { userToken } = useUserStore();
const config = useRuntimeConfig();
const { data: recipies } = await useFetch(request, {
  key: String(Math.random()),
  baseURL: config.public.baseURL,
  headers: { authorization: "Bearer " + userToken },
});
</script>
