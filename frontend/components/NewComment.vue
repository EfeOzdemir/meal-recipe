<template>
  <Card class="w-full mt-12 mx-auto">
    <CardContent class="flex items-end mt-4 justify-between">
      <form class="flex w-4/5">
        <div class="grid items-center w-full gap-4">
          <div class="flex flex-col space-y-1.5">
            <Label for="name">Comment</Label>
            <Input
              id="content"
              placeholder="Type your opinion"
              v-model="content"
            />
          </div>
        </div>
      </form>
      <div>
        <Button class="w-[150px]" @click="send">Send</Button>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
const props = defineProps(["id"]);
const emit = defineEmits(['newcomment'])
const store = useUserStore();
const content = ref("");
const send = async () => {
  const data = await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/comment/" + props.id, {
    method: "post",
    headers: { authorization: "Bearer " + store.userToken },
    body: JSON.stringify({
      content: content.value,
    }),
  });
  emit("newcomment", data)
  content.value = ""
};
</script>
