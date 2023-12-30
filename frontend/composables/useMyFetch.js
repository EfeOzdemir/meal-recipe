export const useMyFetch = (request, opts) => {
  const { userToken } = useUserStore();
  const config = useRuntimeConfig();

  return useFetch(request, {
    baseURL: config.public.baseURL,
    ...opts,
    headers: { authorization: "Bearer " + userToken },
  });
};
