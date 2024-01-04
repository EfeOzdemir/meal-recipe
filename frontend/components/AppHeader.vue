<template>
  <header
    class="flex items-center justify-between h-16 border-b px-40 bg-[#B31312]"
  >
    <span class="mx-4 font-bold text-3xl text-[#FAF6F0]">COOK</span>
    <LoginModal v-if="!store.userToken" />
    <div v-else class="flex space-x-10 mr-10 items-center">
      <Avatar>
        <AvatarImage src="https://github.com/radix-vue.png" alt="@radix-vue" />
        <AvatarFallback>CN</AvatarFallback>
      </Avatar>
    </div>
  </header>
</template>

<script setup>
import { useUserStore } from "~/stores/auth";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
const store = useUserStore();
</script>
