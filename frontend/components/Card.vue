<template>
  <div style="cursor: pointer" class="flex flex-col w-[352px] h-[486px] p-4 bg-white border border-[#E6E6E6] rounded-xl">
    <img loading="lazy" :src="recipe.image" 
      class="w-[320px] h-[320px] rounded-md" />
    <div
      class="categories flex flex-row justify-center space-x-2 text-center text-[#A5A5A5] font-bold text-xs mt-4"
    >
      <div class="flex border border-[#E6E6E6] rounded h-[22px] px-2 items-center ">
        {{ recipe.category.name || "category" }}
      </div>
    </div>
    <h3 class="text-xl text-center text-primary-100 font-semibold mt-3">
      {{ recipe.title }}
    </h3>
    <h4 class="text-center text-primary-100 mt-3">
      {{ recipe.user.username }}
    </h4>
    <div class="flex justify-end">
      <div class="space-x-2">
        <ClientOnly>
          <font-awesome-icon v-if="!liked" @click="like()" icon="fa-regular fa-heart" />
          <font-awesome-icon v-if="liked" @click="like()" icon="fa-solid fa-heart" />
          <font-awesome-icon v-if="!saved" @click="save()" icon="fa-regular fa-bookmark" />
          <font-awesome-icon v-if="saved" @click="save()" icon="fa-solid fa-bookmark" />
        </ClientOnly>
      </div>
    </div>
    <NuxtLink :to="`/${recipe.id}`">
      <Button class="mt-3 w-[320px] h-10 items-center justify-center bg-[#EEE2DE] rounded-md font-bold"> Detail </Button>
    </NuxtLink>
  </div>
</template>

<script>
import Button from "./ui/button/Button.vue";

export default {
  components: { Button },
  props: {
    recipe: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const liked = ref(false);
    const saved = ref(false);
    const store = useUserStore();

    const like = async () => {
      await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/like/" + props.recipe.id, {
        method: "post",
        headers: { authorization: "Bearer " + store.userToken },
      });
      liked.value = !liked.value;
    };
    const save = async () => {
      await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/save/" + props.recipe.id, {
        method: "post",
        headers: { authorization: "Bearer " + store.userToken },
      });
      saved.value = !saved.value;
    };
    return { liked, saved, like, save };
  },
};
</script>

<style lang="scss" scoped></style>
