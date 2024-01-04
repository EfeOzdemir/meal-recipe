<template>
  <div
    class="flex content-center py-2 px-20 border justify-between w-4/5 border rounded-lg m-auto max-w-[1400px] mt-4"
  >
    <div class="flex items-center space-x-2">
      <Select>
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Select a category" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel>Fruits</SelectLabel>
            <SelectItem value="apple"> Apple </SelectItem>
            <SelectItem value="banana"> Banana </SelectItem>
            <SelectItem value="blueberry"> Blueberry </SelectItem>
            <SelectItem value="grapes"> Grapes </SelectItem>
            <SelectItem value="pineapple"> Pineapple </SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
      <SelectRoot v-model="category_id">
        <SelectTrigger class="w-[180px]">
          <SelectValue placeholder="Select a category" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectItem v-for="category in categories" :value="category.id">
              {{ category.name }}
            </SelectItem>
          </SelectGroup>
        </SelectContent>
      </SelectRoot>
      <Button type="submit" @click="filter">
        Apply Filter
      </Button>
    </div>
    <NewRecipeModal v-if="store?.userToken" />
  </div>
</template>

<script setup lang="ts">
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { SelectRoot } from "radix-vue";
const store = useUserStore();
const category_id = ref();

const categories = await $fetch("http://127.0.0.1:5000/recipe/category");

const filter = async () => {
  await navigateTo('?c=' + category_id.value)
}

</script>
