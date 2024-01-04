<template>
  <div class="max-w-[1100px] mx-auto">
    <img
      loading="lazy"
      src="https://i.nefisyemektarifleri.com/2023/12/27/pismeyen-tart-pasta.jpg"
      class="rounded-md mx-auto mt-8"
    />
    <div
      class="categories flex flex-row justify-center space-x-2 text-center text-[#A5A5A5] font-bold text-xs mt-4"
    >
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
      {{ recipe?.cre_date.split(" ")[0] }}
    </h4>
    <div class="flex justify-end">
      <div class="space-x-2">
        <ClientOnly>
          <font-awesome-icon
            v-if="!liked"
            @click="like"
            icon="fa-regular fa-heart"
          />

          <font-awesome-icon
            v-if="liked"
            @click="like"
            icon="fa-solid fa-heart"
          />
          <font-awesome-icon
            v-if="!saved"
            @click="save"
            icon="fa-regular fa-bookmark"
          />
          <font-awesome-icon
            v-if="saved"
            @click="save"
            icon="fa-solid fa-bookmark"
          />
        </ClientOnly>
      </div>
    </div>
    <div>
      <span class="font-bold text-xl">{{ recipe?.title }} Nasıl Yapılır?</span>
      <br />
      <br />
      {{ recipe?.content }}
    </div>
    <CommentList :comments="recipe?.comments" />
    <ClientOnly>
      <CommentList :comments="recipe?.comments" />
      <NewComment :id="recipe?.id" v-if="store.userToken" @get="getDetails"/>
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
      async () => await $fetch("http://127.0.0.1:5000/recipe/" + slug)
    );

    const liked = ref(false);
    const saved = ref(false);

    const like = async () => {
      await $fetch("http://localhost:5000/recipe/like/" + slug, {
        method: "post",
        headers: { authorization: "Bearer " + store.userToken },
      });
      liked.value = !liked.value;
    };
    const save = async () => {
      await $fetch("http://localhost:5000/recipe/save/" + slug, {
        method: "post",
        headers: { authorization: "Bearer " + store.userToken },
      });
      saved.value = !saved.value;
    };
    console.log(recipe);
    return { like, save, liked, saved, recipe, store };
  },
};
</script>

<style scoped></style>
