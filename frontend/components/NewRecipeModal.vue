<template>
  <DialogRoot v-model:open="show" :modal="true">
    <DialogTrigger as-child @click="getCategories">
      <Button class="w-16 h-10 items-center justify-center bg-[#3D3B40] text-[#FAF6F0] rounded-md">Add</Button>
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>New Recipe</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid w-full gap-1.5">
          <Label for="title">Title</Label>
          <Input id="title" type="text" v-model="recipe.title" placeholder="title" />
        </div>
        <div class="grid w-full gap-1.5">
          <Label for="content">Content</Label>
          <Textarea class="h-[150px]" v-model="recipe.content" id="content" placeholder="Type your content here." />
        </div>
        <div class="grid w-full gap-1.5">
          <Label for="ingredients">Ingredients</Label>
          <Input id="ingredients" type="text" v-model="recipe.ingredients" placeholder="Ingredient1, Ingredient2, ..." />
        </div>

        <div class="grid w-full gap-1.5">
          <Label for="content">Category</Label>
          <Select v-model="recipe.category_id">
            <SelectTrigger>
              <SelectValue placeholder="Select a category" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem v-for="category in categories" :value="category.id">
                  {{ category.name }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div class="grid w-full items-center gap-1.5">
          <Label for="picture">Picture</Label>
          <Input @change="handleFileChange" accept="image/*" id="picture" type="file" />
        </div>
      </div>
      <DialogFooter>
        <Button type="submit" @click="add"> Post </Button>
      </DialogFooter>
    </DialogContent>
  </DialogRoot>
</template>
<script setup>
import { Textarea } from '@/components/ui/textarea';
import { DialogRoot } from 'radix-vue';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const store = useUserStore();
const show = ref(false);
const recipe = ref({});
const categories = ref([]);
const file = ref(null);

const getCategories = async () => {
  const category = await $fetch('https://hopeful-vim-417109.oa.r.appspot.com/recipe/category');
  categories.value = category;
};

const handleFileChange = (event) => {
  file.value = event.target.files[0];
};

const add = async () => {
  if (!recipe.value.title || !recipe.value.content || !recipe.value.category_id || !file.value) {
    alert('Fill empty fields.');
    return;
  }

  const formData = new FormData();
  formData.append('title', recipe.value.title);
  formData.append('content', recipe.value.content);
  formData.append('category_id', recipe.value.category_id);
  formData.append('ingredients', recipe.value.ingredients);
  formData.append('image', file.value);

  await $fetch('https://hopeful-vim-417109.oa.r.appspot.com/recipe/', {
    method: 'post',
    headers: { authorization: 'Bearer ' + store.userToken },
    body: formData,
  });
  show.value = false;
  window.location.reload();
};
</script>