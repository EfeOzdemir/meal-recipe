<template>
  <div
    class="flex content-center py-2 px-20 border justify-between w-4/5 border rounded-lg m-auto max-w-[1400px] mt-4"
    style="background-color: #d8d3cd"
  >
    <div class="flex items-center space-x-2">
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
      <Button class="w-32 h-10 items-center justify-center bg-[#3D3B40] text-[#FAF6F0] rounded-md" type="submit" @click="filter">
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
