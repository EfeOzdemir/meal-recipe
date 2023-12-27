<template>
    <DialogRoot v-model:open="show">
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
                <Button type="submit" @click="submit()">
                    Login
                </Button>
            </DialogFooter>
        </DialogContent>
    </DialogRoot>
</template>
<script setup>

import { CircleUserRound } from 'lucide-vue-next';
import { DialogRoot } from 'radix-vue';


</script>