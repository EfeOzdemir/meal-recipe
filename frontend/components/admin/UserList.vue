<template>
    <div class="w-4/5 m-auto">
        <div class="flex w-full mt-16 justify-end">
            <Button @click="async () => await navigateTo('/admin/users/create')">New User</Button>
        </div>
        <Table class="mt-4 border-4">
            <TableCaption>User list.</TableCaption>
            <TableHeader>
                <TableRow>
                    <TableHead class="w-[100px]">
                        User Id
                    </TableHead>
                    <TableHead>Username</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Password</TableHead>
                    <TableHead></TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                <TableRow v-for="user in users" :key="user.id">
                    <TableCell class="font-medium">
                        {{ user.id }}
                    </TableCell>
                    <TableCell>{{ user.username }}</TableCell>
                    <TableCell>{{ user.email }}</TableCell>
                    <TableCell>{{ user.password.substring(100) + '...' }}</TableCell>
                    <TableCell>
                        <DropdownMenu>
                            <DropdownMenuTrigger>
                                <font-awesome-icon icon="fa-solid fa-ellipsis" />
                            </DropdownMenuTrigger>
                            <DropdownMenuContent>
                                <DropdownMenuItem @click="async () => await navigateTo('/admin/users/edit/' + user.id)">Edit
                                </DropdownMenuItem>
                                <DropdownMenuItem @click="deleteUser(user.id)">Delete</DropdownMenuItem>
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

const users = ref([])

const getUsers = async () => {
    const data = await $fetch('http://localhost:5000/admin/users')
    users.value = data
}

const deleteUser = async (id) => {
    await $fetch('http://localhost:5000/admin/user/delete/' + id, { method: "DELETE" })
    getUsers()
}

onMounted(() => {
    getUsers()
})
</script>
