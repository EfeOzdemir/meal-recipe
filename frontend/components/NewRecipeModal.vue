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
      </div>
      <DialogFooter>
        <Button type="submit" @click="add"> Post </Button>
      </DialogFooter>
    </DialogContent>
  </DialogRoot>
</template>
<script setup>
import { Textarea } from "@/components/ui/textarea";
import { DialogRoot } from "radix-vue";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const store = useUserStore();
const show = ref(false);
const recipe = ref({});
const categories = ref([]);

const getCategories = async () => {
  const category = await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/category");
  categories.value = category;
};

const add = async () => {

  if (!recipe.value.title || !recipe.value.content || !recipe.value.category_id) {
    alert("Fill empty fields.")
    return
  }

  await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/", {
    method: "post",
    headers: { authorization: "Bearer " + store.userToken },
    body: JSON.stringify({
      title: recipe.value.title,
      content: recipe.value.content,
      category_id: recipe.value.category_id,
      ingredients: ["su"],
    }),
  });
  show.value = false;
  window.location.reload();
};
</script>
