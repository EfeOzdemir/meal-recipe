<template>
  <DialogRoot v-model:open="show" :modal="true">
    <DialogTrigger as-child>
      <Button>Add</Button>
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>New Recipe</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid w-full gap-1.5">
          <Label for="title">Title</Label>
          <Input
            id="title"
            type="text"
            v-model="recipe.title"
            placeholder="title"
          />
        </div>
        <div class="grid w-full gap-1.5">
          <Label for="content">Content</Label>
          <Textarea
            class="h-[150px]"
            v-model="recipe.content"
            id="content"
            placeholder="Type your content here."
          />
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

const show = ref(false);
const recipe = ref({});
const { data: categories } = await useMyFetch("/recipe/category", {
  method: "get",
});
const add = async () => {
  const { data, error } = await useMyFetch("/recipe/", {
    method: "post",
    server: false,
    lazy: true,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: recipe.value.title,
      content: recipe.value.content,
      category_id: recipe.value.category_id,
      ingredients: [1],
    }),
  });
  show.value = false;
};
</script>
