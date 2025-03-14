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

// Load findings from a test results.
export function loadFindings(proxyObject: object) {
  const findings = [];
  // TODO(Kyle): Standardize conversion of proxy objects.
  const test_results = JSON.parse(JSON.stringify(proxyObject));
  const results = test_results.body.results;
  console.log(results);
  for (let key in results) {
    console.log(key);
    const result = results[key];
    console.log(result);
    const finding = {
      status: result.type,
      measurement: result.evidence_metadata.measurement.measurement_class,
      test_case_id: result.evidence_metadata.test_case_id.name,
      message: result.message,
    };
    findings.push(finding);
  }
  console.log("termine")
  console.log(findings)
  return findings;
}
