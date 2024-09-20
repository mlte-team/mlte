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

// Load findings from a validated specication.
export function loadFindings(proxyObject: object) {
  console.log("loading findings");
  const findings = [];
  // TODO(Kyle): Standardize conversion of proxy objects.
  const validatedSpec = JSON.parse(JSON.stringify(proxyObject));
  validatedSpec.body.spec.properties.forEach((property) => {
    // TODO(Kyle): This is not portable to some browsers.
    const results = new Map(
      Object.entries(validatedSpec.body.results[property.name]),
    );
    results.forEach((value) => {
      const finding = {
        status: value.type,
        property: property.name,
        measurement: value.metadata.measurement_type,
        evidence_id: value.metadata.identifier.name,
        message: value.message,
      };
      findings.push(finding);
    });
  });
  return findings;
}
