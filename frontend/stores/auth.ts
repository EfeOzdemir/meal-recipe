export const useUserStore = defineStore("user", () => {
  const isLoggedin = ref(false);
  const userToken = ref<String | null>(null);
  const user = ref<UserInfo | null>(null);
  const cookie = useCookie<String | null>("token", {
    maxAge: 60 * 60 * 24 * 30,
  });
  if (cookie.value) {
    userToken.value = cookie.value;
    isLoggedin.value = true;
  }
  const login = async (username: string, password: string) => {
    const { data, error } = await useMyFetch("/auth/login", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    if (data) {
      isLoggedin.value = true;
      const response = data.value;
      cookie.value = response.token;
      userToken.value = response.token;
    } else {
      isLoggedin.value = false;
      user.value = null;
      return false;
    }
  };
  const logout = () => {
    isLoggedin.value = false;
    user.value = null;
    cookie.value = null;
  };
  return { isLoggedin, user, login, logout, userToken };
});

interface UserInfo {
  id: number;
  name: string;
  password: string;
}
