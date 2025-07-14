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
