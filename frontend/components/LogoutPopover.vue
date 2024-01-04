<template>
  <Popover>
    <PopoverTrigger as-child>
      <div class="flex space-x-10 mr-10 items-center">
        <Avatar>
          <AvatarImage src="https://github.com/radix-vue.png" alt="@radix-vue" />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
      </div>
    </PopoverTrigger>
    <PopoverContent class="w-80">
      <div class="flex justify-between">
        <div class="space-y-2">
          <h4 class="font-medium leading-none">
            {{ user?.name }}
          </h4>
          <p class="text-sm text-muted-foreground">Hoşgeldin</p>
        </div>
        <div class="flex">
          <div class="items-center">
            <Button @click="logout_">Çıkış yap</Button>
          </div>
        </div>
      </div>
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "./ui/button";
import { useUserStore } from "@/stores/auth";

const { logout, user } = useUserStore();

const logout_ = async () => {
  logout()
  window.location.href = '/' 
}
</script>
