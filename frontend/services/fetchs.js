export const fetchRecipes = () => {
  return useMyFetch("/recipe", {
    method: "get",
  });
};
