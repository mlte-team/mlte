const config = useRuntimeConfig();

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

export async function loadReportData(
  token: string,
  model: string,
  version: string,
  artifactId: string,
): Promise<ReportModel> {
  const { data: reportData, error } = await useFetch<ReportApiResponse>(
    config.public.apiPath +
      "/model/" +
      model +
      "/version/" +
      version +
      "/artifact/" +
      artifactId,
    {
      retry: 0,
      method: "GET",
      headers: {
        Authorization: "Bearer " + token,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
  if (!error.value && reportData.value && isValidReport(reportData.value)) {
    const reportModel: ReportModel = reportData.value.body;
    return reportModel;
  } else {
    return new ReportModel();
  }
}

// Load findings from a test results.
export function loadFindings(
  testResults: TestResultsModel,
  system_requirements: Array<QASDescriptor>,
): Array<Finding> {
  const findings: Array<Finding> = [];
  const results = testResults.results;
  const test_cases = testResults.test_suite.test_cases;
  for (const key in results) {
    const result = results[key];
    const matched_test_case = test_cases.find(
      (x) => x.identifier === result.evidence_metadata.test_case_id,
    );

    if (matched_test_case === undefined) {
      console.log(
        "Error: Test case identifier did not match a result test_case_id.",
      );
      continue;
    }

    const new_qas_list: Array<QualityAttributeScenario> = [];
    matched_test_case.qas_list.forEach((qas_id) => {
      const matched_req = system_requirements.find(
        (x) => x.identifier === qas_id,
      );
      new_qas_list.push({
        id: qas_id,
        qa: matched_req!.quality,
      });
    });

    const finding = new Finding(
      result.type,
      result.evidence_metadata.measurement.measurement_class,
      result.evidence_metadata.test_case_id,
      result.message,
      new_qas_list,
    );
    findings.push(finding);
  }
  return findings;
}

export async function loadTestResults(
  token: string,
  model: string,
  version: string,
  test_results_id: string,
  system_requirements: Array<QASDescriptor>,
): Promise<Array<Finding>> {
  const testResultsRes = await fetchArtifact(
    token as string,
    model as string,
    version as string,
    test_results_id,
  );

  // TODO : Consider error handling
  if (testResultsRes.body.artifact_type === "test_results") {
    return loadFindings(
      testResultsRes.body as TestResultsModel,
      system_requirements,
    );
  } else {
    return [];
  }
}
