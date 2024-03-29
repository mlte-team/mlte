export function unsuccessfulLogin() {
  alert("Incorrect username or password.");
}

export function confirmLogout() {
  const token = useCookie("token");
  if (
    confirm(
      "Are you sure you want to logout? All unsaved changes wll be lost. ",
    )
  ) {
    token.value = undefined;
    navigateTo("/login");
  }
}
