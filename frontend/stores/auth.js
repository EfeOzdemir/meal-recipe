export const useUserStore = defineStore("user", () => {
  const isLoggedin = ref(false);
  const userToken = ref(null);
  const user = ref(null);
  const cookie = useCookie("token", {
    maxAge: 60 * 60 * 24 * 30,
  });

  if (cookie.value) {
    userToken.value = cookie.value;
    isLoggedin.value = true;
  }
  
  const login = async (username, password) => {
    const response = await $fetch("https://hopeful-vim-417109.oa.r.appspot.com/auth/login", {
      method: "POST",
      body: {
        username: username,
        password: password,
      },
    }).catch((err) => console.log(err.data));

    if (response) {
      userToken.value = response.token;
      isLoggedin.value = true;
      cookie.value = response.token;
    }
  };
  const logout = () => {
    isLoggedin.value = false;
    user.value = null;
    cookie.value = null;
  };
  return { isLoggedin, user, login, logout, userToken };
});
