<template>
  <header class="flex items-center justify-between h-16 border-b">
    <span class="mx-4 font-bold text-3xl">COOK</span>
    {{ store.userToken || "none" }}
    <LoginModal />
  </header>
</template>

<script setup>
import { useUserStore } from "~/stores/userStore";

const store = useUserStore();
</script>
