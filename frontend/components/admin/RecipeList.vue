<template>
    <div class="w-4/5 m-auto">
        <div class="flex w-full mt-16 justify-end">
            <Button @click="async () => await navigateTo('/admin/recipies/create')">New Recipie</Button>
        </div>
        <Table class="mt-4 border-4">
            <TableCaption>Recipe list.</TableCaption>
            <TableHeader>
                <TableRow>
                    <TableHead class="w-[100px]">
                        Recipe Id
                    </TableHead>
                    <TableHead>Title</TableHead>
                    <TableHead>Content</TableHead>
                    <TableHead>Cre By</TableHead>
                    <TableHead>Cre Date</TableHead>
                    <TableHead></TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                <TableRow v-for="recipe in recipies" :key="recipe.id">
                    <TableCell class="font-medium">
                        {{ recipe.id }}
                    </TableCell>
                    <TableCell>{{ recipe.title }}</TableCell>
                    <TableCell>{{ recipe.content.substring(0, 100) + '...' }}</TableCell>
                    <TableCell>{{ recipe.user.username || 'Admin' }}</TableCell>
                    <TableCell>{{ recipe.cre_date }}</TableCell>
                    <TableCell>
                        <DropdownMenu>
                            <DropdownMenuTrigger>
                                <font-awesome-icon icon="fa-solid fa-ellipsis" />
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                                <DropdownMenuItem @click="async () => await navigateTo('/admin/recipies/edit/' + recipe.id)">Edit
                                </DropdownMenuItem>
                                <DropdownMenuItem @click="deleteRecipe(recipe.id)">Delete</DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </TableCell>
                </TableRow>
            </TableBody>
        </Table>
    </div>
</template>

<script setup>
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import Button from '../ui/button/Button.vue';

const recipies = ref([])

const getRecipies = async () => {
    const data = await $fetch('https://hopeful-vim-417109.oa.r.appspot.com/recipe/')
    recipies.value = data
}

const deleteRecipe = async (id) => {
    await $fetch('https://hopeful-vim-417109.oa.r.appspot.com/admin/recipe/delete/' + id, { method: "DELETE" })
    getRecipies()
}

onMounted(() => {
    getRecipies()
})
</script>
