<template>
    <DialogRoot v-model:open="show" :modal="true">
        <DialogTrigger as-child>
            <CircleUserRound class="mr-4" />
        </DialogTrigger>
        <DialogContent class="sm:max-w-[425px]">
            <DialogHeader>
                <DialogTitle>Log In</DialogTitle>
            </DialogHeader>
            <div class="grid gap-4 py-4">
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="username" class="text-right">
                        Username
                    </Label>
                    <Input id="username" v-model="username" class="col-span-3" />
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="current" class="text-right">Password</Label>
                    <Input id="current" type="password" v-model="password" class="col-span-3" />
                </div>
            </div>
            <DialogFooter>
                <Button type="submit" @click="login">
                    Login
                </Button>
            </DialogFooter>
        </DialogContent>
    </DialogRoot>
</template>
<script setup>

import { useFetch } from '@vueuse/core';
import { CircleUserRound } from 'lucide-vue-next';
import { DialogRoot } from 'radix-vue';

const username = ref('')
const password = ref('')

const userStore = useUserStore()
const show = ref(false)

const login = async () => {
    const { data, error } = await useFetch("http://localhost:5000/auth/login", {
        method: 'post',
        headers: { 
            "Content-Type": "application/json",
        },
        body: JSON.stringify({  
            username: username.value,
            password: password.value
        })
    })
    
    if(data) {
        const response = JSON.parse(data.value)
        userStore.userToken = response.token
    }

    show.value = false
}
</script>