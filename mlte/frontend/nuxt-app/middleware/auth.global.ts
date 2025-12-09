export default defineNuxtRouteMiddleware((from) => {
  const token = useCookie("token");

  // Handle unlogged in user, and logged in user going to login page
  if (!token.value && from.fullPath !== "/login") {
    return navigateTo("/login");
  } else if (token.value && from.fullPath === "/login") {
    return navigateTo("/");
  }

  // Handle non-admin accessing admin pages
  const role = useCookie("userRole");
  if (
    token.value &&
    role.value !== "admin" &&
    from.fullPath.substring(0, 7) == "/admin/"
  ) {
    return navigateTo("/");
  }
});
