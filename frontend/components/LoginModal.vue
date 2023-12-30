<template>
  <DialogRoot v-model:open="show" :modal="true">
    <DialogTrigger as-child>
      <CircleUserRound class="mr-4" />
    </DialogTrigger>
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Sign In</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="username" class="text-right"> Username </Label>
          <Input id="username" v-model="username" class="col-span-3" />
        </div>
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="current" class="text-right">Password</Label>
          <Input
            id="current"
            type="password"
            v-model="password"
            class="col-span-3"
          />
        </div>
      </div>
      <DialogFooter>
        <Button type="submit" @click="login"> Sign in </Button>
      </DialogFooter>
      <DialogHeader>
        <DialogTitle>Sign up</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="username" class="text-right"> Username </Label>
          <Input id="username" v-model="usernameRegister" class="col-span-3" />
        </div>
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="current" class="text-right">Password</Label>
          <Input
            id="current"
            type="password"
            v-model="passwordRegister"
            class="col-span-3"
          />
        </div>
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="current" class="text-right">Email</Label>
          <Input id="current" type="email" v-model="email" class="col-span-3" />
        </div>
      </div>
      <DialogFooter>
        <Button type="submit" @click="signup"> Sign Up </Button>
      </DialogFooter>
    </DialogContent>
  </DialogRoot>
</template>
<script setup>
import { useFetch } from "@vueuse/core";
import { CircleUserRound } from "lucide-vue-next";
import { DialogRoot } from "radix-vue";
import { useMyFetch } from "@/composables/useMyFetch";

const username = ref("");
const usernameRegister = ref("");
const password = ref("");
const passwordRegister = ref("");
const email = ref("");

const userStore = useUserStore();
const show = ref(false);

const login = async () => {
  const { data, error } = await useMyFetch("/auth/login", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  });

  if (data) {
    const response = data.value;
    userStore.userToken = response.token;
  }

  show.value = false;
};
const signup = async () => {
  const { data, error } = await useMyFetch("/auth/register", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: usernameRegister.value,
      password: passwordRegister.value,
      email: email.value,
    }),
  });

  if (data) {
    username.value = usernameRegister.value;
    password.value = passwordRegister.value;
    await login();
  }

  show.value = false;
};
</script>
