<template>
  <div class="max-w-[1100px] mx-auto">
    <img
      loading="lazy"
      src="https://i.nefisyemektarifleri.com/2023/12/27/pismeyen-tart-pasta.jpg"
      class="rounded-md mx-auto mt-8"
    />
    <div
      class="categories flex flex-row justify-center space-x-2 text-center text-[#A5A5A5] font-bold text-xs mt-4 u-center"
    >
      {{ recipe?.categories }}
    </div>
    <h3 class="text-xl font-bold text-center mt-3 bg-red-300 py-5">
      {{ recipe?.title }}
    </h3>
    <h4 class="text-left mt-3">
      Writer:
      {{ recipe?.user.username }}
    </h4>
    <h4 class="text-left mt-3">
      Creation Date:
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
      {{ recipe?.title }} Nasıl Yapılır?
      <br />
      <br />
      {{ recipe?.content }}
    </div>
    <CommentList :comments="recipe?.comments" />
    <ClientOnly>
      <NewComment :id="recipe?.id" />
    </ClientOnly>
  </div>
</template>

<script>
export default {
  setup() {
    const route = useRoute();
    const slug = route.params.id;
    const { data: recipe } = useAsyncData(
      slug,
      async () => await $fetch("http://127.0.0.1:5000/recipe/" + slug)
    );
    const liked = ref(false);
    const saved = ref(false);
    const store = useUserStore();

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
    return { like, save, liked, saved, recipe };
  },
};
</script>

<style scoped></style>
