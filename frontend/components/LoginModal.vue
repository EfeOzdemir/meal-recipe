<template>
  <DialogRoot v-model:open="show" :modal="true">
    <DialogTrigger as-child>
      <CircleUserRound class="mr-4" />
    </DialogTrigger>
    <DialogContent class="sm:max-w-[425px]">
      <Tabs default-value="signin">
        <TabsList>
          <TabsTrigger value="signin"> Sign In </TabsTrigger>
          <TabsTrigger value="signup"> Sign Up </TabsTrigger>
        </TabsList>
        <TabsContent value="signin">
          <DialogHeader>
            <DialogTitle>Sign In</DialogTitle>
          </DialogHeader>
          <div class="grid gap-4 py-4">
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="username_login" class="text-right"> Username </Label>
              <Input id="username_login" v-model="username" class="col-span-3" />
            </div>
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="password_login" class="text-right">Password</Label>
              <Input id="password_login" type="password" v-model="password" class="col-span-3" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" @click="close"> Sign in </Button>
          </DialogFooter>
        </TabsContent>
        <TabsContent value="signup">
          <DialogHeader>
            <DialogTitle>Sign up</DialogTitle>
          </DialogHeader>
          <div class="grid gap-4 py-4">
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="username_register" class="text-right">
                Username
              </Label>
              <Input id="username_register" v-model="usernameRegister" class="col-span-3" />
            </div>
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="password_register" class="text-right">Password</Label>
              <Input id="password_register" type="password" v-model="passwordRegister" class="col-span-3" />
            </div>
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="email" class="text-right">Email</Label>
              <Input id="email" type="email" v-model="email" class="col-span-3" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" @click="signup"> Sign Up </Button>
          </DialogFooter>
        </TabsContent>
      </Tabs>
    </DialogContent>
  </DialogRoot>
</template>
<script setup>
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CircleUserRound } from "lucide-vue-next";
import { DialogRoot } from "radix-vue";
import { useMyFetch } from "@/composables/useMyFetch";
import { useUserStore } from "@/stores/auth";

const store = useUserStore();
const { login } = store;

const username = ref("");
const usernameRegister = ref("");
const password = ref("");
const passwordRegister = ref("");
const email = ref("");

const show = ref(false);

const close = () => {
  if (!username.value || !password.value) {
    alert("Fill empty fields.")
    return
  }
  login(username.value, password.value);
  show.value = false;
};

const signup = async () => {

  if (!usernameRegister.value || !passwordRegister.value || !email.value) {
    alert("Fill empty fields.")
    return
  }

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
    await login(usernameRegister.value, passwordRegister.value);
  }

  show.value = false;
};
</script>
