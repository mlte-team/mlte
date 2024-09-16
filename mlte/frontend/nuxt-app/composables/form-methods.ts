export function successfulArtifactSubmission(
  artifactType: string,
  artifactName: string,
) {
  alert(`${artifactType}, ${artifactName}, has been saved successfully.`);
}

export function inputErrorAlert() {
  alert("One or more invalid fields in submission.");
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
