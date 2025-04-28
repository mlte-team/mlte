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
export function loadFindings(
  proxyObject: object,
  system_requirements: Array<object>,
) {
  const findings = [];
  // TODO(Kyle): Standardize conversion of proxy objects.
  const test_results = JSON.parse(JSON.stringify(proxyObject));
  const results = test_results.body.results;
  const test_cases = test_results.body.test_suite.test_cases;
  for (const key in results) {
    const result = results[key];
    const matched_case = test_cases.find(
      (x) => x.identifier === result.evidence_metadata.test_case_id,
    );
    const finding = {
      status: result.type,
      measurement: result.evidence_metadata.measurement.measurement_class,
      test_case_id: result.evidence_metadata.test_case_id,
      message: result.message,
      qas_list: matched_case.qas_list,
    };

    findings.push(finding);
  }
  findings.forEach((finding) => {
    const new_qas_list = [];
    finding.qas_list.forEach((qas_id) => {
      const matched_req = system_requirements.find(
        (x) => x.identifier === qas_id,
      );
      new_qas_list.push({
        id: qas_id,
        qa: matched_req.quality,
      });
    });
    finding.qas_list = new_qas_list;
  });
  console.log(findings);

  return findings;
}
