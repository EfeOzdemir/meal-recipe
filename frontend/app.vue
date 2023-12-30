<template>
  <AppHeader/>
  <CardList/>
  <Button @click="fetch" />
</template>

<script setup>
import AppHeader from './components/AppHeader.vue';
const fetch = async() =>{
  const { data, error } = await useMyFetch("/recipe", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: 'asd',
      content: 'sdsadasd',
      category_id: 3,
      ingredients: [1]
    }),
  });

  if (data) {
    console.log(data)
  }

}
</script>
