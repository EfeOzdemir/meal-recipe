<template>
    <Header />
    <Card class="w-3/5 mt-28 mx-auto">
        <CardHeader>
            <CardTitle>New Recipe</CardTitle>
            <CardDescription>Add new recipe.</CardDescription>
        </CardHeader>
        <CardContent>
            <form>
                <div class="grid items-center w-full gap-4">
                    <div class="flex flex-col space-y-1.5">
                        <Label for="title">Title</Label>
                        <Input id="title" placeholder="Title" v-model="recipe.title" />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="content">Content</Label>
                        <Textarea class="h-[150px]" placeholder="Type your content here." v-model="recipe.content" />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="category">Category</Label>
                        <SelectRoot v-model="recipe.category_id">
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
                    </div>
                </div>
            </form>
        </CardContent>
        <CardFooter class="flex justify-end px-6 pb-6 space-x-2">
            <Button @click="save">Save</Button>
            <Button @click="async () => {
                await navigateTo('/admin/recipies')
            }">Cancel</Button>
        </CardFooter>
    </Card>
</template>

<script setup lang='ts'>
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import Header from '~/components/admin/Header.vue';
import {
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { SelectRoot } from 'radix-vue';

const recipe = ref({})
const categories = ref([])

const save = async () => {
    recipe.value.ingredients = [1]
    console.log(recipe.value)
    await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/admin/recipe/create", {
        method: "post",
        body: JSON.stringify(recipe.value)
    })
    await navigateTo('/admin/recipies')
}

const getCategories = async () => {
    const categoriesData = await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/category")
    categories.value = categoriesData
}

onMounted(() => {
    getCategories()
})

</script>