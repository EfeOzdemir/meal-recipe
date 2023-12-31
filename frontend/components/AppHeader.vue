<template>
  <header class="flex items-center justify-between h-16 border-b px-40">
    <span class="mx-4 font-bold text-3xl">COOK</span>
    <LoginModal v-if="!store.userToken" />
    <div v-else class="flex space-x-10 mr-10 items-center">
      <ClientOnly>
        <font-awesome-icon icon="fa-solid fa-heart" />
        <font-awesome-icon icon="fa-solid fa-bookmark" />
      </ClientOnly>
      <Avatar>
        <AvatarImage src="https://github.com/radix-vue.png" alt="@radix-vue" />
        <AvatarFallback>CN</AvatarFallback>
      </Avatar>
    </div>
  </header>
</template>

<script setup>
import { useUserStore } from "~/stores/auth";
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
const store = useUserStore();
</script>
