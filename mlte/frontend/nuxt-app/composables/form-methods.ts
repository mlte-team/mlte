export function successfulArtifactSubmission(
  artifactType: string,
  artifactName: string,
) {
  alert(`Your ${artifactType}, ${artifactName}, has been saved successfully.`);
}

export function cancelFormSubmission(redirect: string) {
  if (
    confirm(
      "Are you sure you want to leave this page? All unsaved changes will be lost.",
    )
  ) {
    location.href = redirect;
  }
}
