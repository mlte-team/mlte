export default defineNuxtRouteMiddleware((from) => {
  const token = useCookie("token");
  if (!token.value && from.fullPath !== "/login-page") {
    return navigateTo("/login-page");
  } else if (token.value && from.fullPath === "/login-page") {
    return navigateTo("/");
  }
});
