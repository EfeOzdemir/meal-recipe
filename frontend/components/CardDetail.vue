<template>
  <div class="max-w-[1100px] mx-auto">
    <img loading="lazy" :src="recipe?.image" class="rounded-md mx-auto mt-8" />
    <div class="categories flex flex-row justify-center space-x-2 text-center text-[#A5A5A5] font-bold text-xs mt-4">
      {{ recipe?.categories }}
    </div>
    <h3 class="text-xl font-bold text-center mt-3 bg-[#EEE2DE] py-5">
      {{ recipe?.title }}
    </h3>
    <h4 class="text-left text-lg mt-3">
      <span class="font-bold">Writer:</span>
      {{ recipe?.user.username }}
    </h4>
    <h4 class="text-left mt-3 text-lg">
      <span class="font-bold">Creation Date:</span>
      {{ recipe?.cre_date }}
    </h4>
    <div class="flex justify-end">
      <div class="space-x-2">
        <ClientOnly>
          <font-awesome-icon v-if="!liked" @click="like" icon="fa-regular fa-heart" />

          <font-awesome-icon v-if="liked" @click="like" icon="fa-solid fa-heart" />
          <font-awesome-icon v-if="!saved" @click="save" icon="fa-regular fa-bookmark" />
          <font-awesome-icon v-if="saved" @click="save" icon="fa-solid fa-bookmark" />
        </ClientOnly>
      </div>
    </div>
    <div>
      <span class="font-bold text-xl">Instructions</span>
      <br />
      {{ recipe?.content }}
      <br />
      <br />
      <span class="font-bold text-xl">Ingredients</span>
      <ul>
        <li v-for="i in recipe?.ingredients?.split(',')">
          <span> -> {{ i }}</span>
        </li>
      </ul>
      <br />
      <br />
    </div>
    <CommentList :comments="recipe?.comments" />
    <ClientOnly>
      <NewComment :id="recipe?.id" v-if="store.userToken" @newcomment="newComment" />
    </ClientOnly>
  </div>
</template>

<script>
export default {
  setup() {
    const store = useUserStore()
    const route = useRoute();
    const slug = route.params.id;

    const { data: recipe } = useAsyncData(
      slug,
      async () => await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/" + slug)
    );

    const liked = ref(false);
    const saved = ref(false);

    const like = async () => {
      await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/like/" + slug, {
        method: "post",
        headers: { authorization: "Bearer " + store.userToken },
      });
      liked.value = !liked.value;
    };
    const save = async () => {
      await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/recipe/save/" + slug, {
        method: "post",
        headers: { authorization: "Bearer " + store.userToken },
      });
      saved.value = !saved.value;
    };

    const newComment = (data) => {
      window.location.reload(true)
    }

    return { like, save, liked, saved, recipe, store, newComment };
  },
};
</script>

<style scoped></style>
