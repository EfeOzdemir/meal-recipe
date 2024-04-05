<template>
  <header
    class="flex items-center justify-between h-16 border-b px-40 bg-[#B31312]"
  >
    <button class="mx-4 font-bold text-3xl text-[#FAF6F0]" @click="func">COOK</button>
    <LoginModal v-if="!store.userToken" />
    <LogoutPopover v-else />

    
  </header>
</template>

<script setup>
import { useUserStore } from "~/stores/auth";
const store = useUserStore();
const func = async () => {
  await navigateTo("/");
  window.location.reload()
}
</script>
