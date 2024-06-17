export function alert400Error(message: string) {
  alert(message);
}

export function successfulSubmission(
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

export function requestErrorAlert() {
  alert(
    "Error encountered while communicating with API. Ensure store is running and allowed-origins is configured correctly.",
  );
}

export function responseErrorAlert() {
  alert(
    "Error encountered in response from API. Check browser and store console for more information.",
  );
}

export function conflictErrorAlert() {
  alert("Name specified for artifact is already in use.");
}
