<template>
    <Header />
    <Card class="w-3/5 mt-28 mx-auto">
        <CardHeader>
            <CardTitle>Edit User</CardTitle>
            <CardDescription>Change user data.</CardDescription>
        </CardHeader>
        <CardContent>
            <form>
                <div class="grid items-center w-full gap-4">
                    <div class="flex flex-col space-y-1.5">
                        <Label for="name">Username</Label>
                        <Input id="name" placeholder="New Username" v-model="user.username" />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="email">Email</Label>
                        <Input id="email" placeholder="New Email" v-model="user.email" />
                    </div>
                    <div class="flex flex-col space-y-1.5">
                        <Label for="password">Password</Label>
                        <Input id="password" placeholder="New Password - Do not fill if you will not change."
                            v-model="user.password" />
                    </div>
                </div>
            </form>
        </CardContent>
        <CardFooter class="flex justify-end px-6 pb-6 space-x-2">
            <Button @click="save">Save</Button>
            <Button @click="async () => {
                await navigateTo('/admin/users')
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
import { onMounted } from 'vue';

const route = useRoute()
const id = route.params.id

const user = ref({})

const getUser = async () => {
    const data = await $fetch("http://localhost:5000/admin/user/" + id)
    user.value = data
}

const save = async () => {
    await $fetch("http://localhost:5000/admin/user/edit/" + user.value.id, {
        method: "post",
        body: JSON.stringify(user.value)
    })
    await navigateTo('/admin/users')
}

onMounted(() => {
    getUser()
})

</script>