<template>
  <div>
    <div v-for="comment in comments" :key="comment.id" class="relative">
      <div class="flex">
        <div class="ml-4 comment-width">
          <div class="font-bold text-md flex items-center justify-between mb-1">
            <div class="w-full flex items-center">
              {{ comment?.user?.username }}
            </div>
          </div>
          <p class="text-sm leading-18 sm:text-md sm:leading-22 break-words">
            {{ comment?.content }}
          </p>
          <div class="text-sm font-medium flex items-center mt-2">
            <time class="text-primary-300 text-sm font-medium ml-auto">{{
              comment?.cre_date
            }}</time>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { comments } = defineProps(["comments"]);
</script>
