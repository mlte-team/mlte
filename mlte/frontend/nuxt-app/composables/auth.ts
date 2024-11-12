export function confirmLogout() {
  const token = useCookie("token");
  const user = useCookie("user");
  const userRole = useCookie("userRole")
  if (
    confirm("Are you sure you want to logout? All unsaved changes wll be lost.")
  ) {
    token.value = undefined;
    user.value = undefined;
    userRole.value = undefined;
    navigateTo("/login");
  }
}
