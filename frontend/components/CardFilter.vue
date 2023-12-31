<template>
  <div class="flex content-center py-2 px-20 border justify-between w-4/5 border rounded-lg m-auto max-w-[1400px] mt-4">
    <div class="flex items-center space-x-2">
      <span>Filter Category</span>
      <span>Filter Ingredient</span>
      <span>{{ store?.userToken }}</span>
    </div>
    <NewRecipeModal v-if="store?.userToken" />
  </div>
</template>

<script setup>
const store = useUserStore();
</script>
