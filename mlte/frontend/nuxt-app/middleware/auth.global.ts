export default defineNuxtRouteMiddleware((from, to) => {
  const token = useCookie("token");
  if(!token.value && from.fullPath != '/login'){
    return navigateTo("/login")
  }
})