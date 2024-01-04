<template>
  <div class="relative todo-fragment">
    <div class="flex">
      <Button pure class="h-11">
        <Avatar>
          <AvatarImage
            src="https://github.com/radix-vue.png"
            alt="@radix-vue"
          />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
      </Button>
      <div class="ml-4 comment-width">
        <header
          class="font-bold text-md flex items-center justify-between mb-1"
        >
          <div class="w-full flex items-center">
            {{ comment.user?.username }}
          </div>
        </header>
        <p class="text-sm leading-18 sm:text-md sm:leading-22 break-words">
          {{ comment.content }}
        </p>
        <div class="text-sm font-medium flex items-center mt-2">
          <time class="text-primary-300 text-sm font-medium ml-auto">{{
            comment.cre_date
          }}</time>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default defineComponent({
  props: ["comment"],
});
</script>

<style></style>
