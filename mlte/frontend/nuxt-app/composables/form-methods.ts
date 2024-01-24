export function cancelFormSubmission(redirect: string) {
  if (
    confirm(
      "Are you sure you want to leave this page? All changes will be lost.",
    )
  ) {
    location.href = redirect;
  }
}