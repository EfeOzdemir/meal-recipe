export const useMyFetch = (request, opts) => {
  const { userToken } = useUserStore();
  const config = useRuntimeConfig();
  console.log(userToken);
  return useFetch(request, {
    baseURL: config.public.baseURL,
    ...opts,
    headers: { authorization: userToken },
  });
};
