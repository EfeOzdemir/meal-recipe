<template>
  <div>
    <Comment v-for="comment in comments" :key="comment.id" />
  </div>
</template>

<script>
export default defineComponent({
  props: ["comments"],
});
</script>

<style scoped></style>
