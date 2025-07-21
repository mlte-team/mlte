import type { NitroFetchOptions } from "nitropack";

const config = useRuntimeConfig();

/**
 * Generic $fetch function for HTTP requests to API.
 *
 * @template T The expected type of the data returned from the API.
 * @param {string} url The URL to fetch data from.
 * @param {string} method HTTP method to use for request
 * @param {string} [token] Token used to authenticate with API.
 * @param {NitroFetchOptions<string>} [options] Optional configuration for $fetch.
 * @returns {Promise<T> | null} Promise that resolves to the data from request or null if there is an error.
 */
export function useApi<T>(
  url: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  token?: string,
  options?: NitroFetchOptions<string>,
): Promise<T> | null {
  const defaultOptions: NitroFetchOptions<string> = {
    baseURL: config.public.apiPath,
    retry: 0,
    method: method,
    onRequestError() {
      requestErrorAlert();
    },
    onResponseError({ response }) {
      const errorMessage = response._data?.error_description || "Unknown error";
      handleHttpError(response?.status || 0, errorMessage);
    },
  };

  if (token) {
    defaultOptions["headers"] = { Authorization: "Bearer " + token };
  }

  // Merge default options with any provided options
  const mergedOptions: NitroFetchOptions<string> = {
    ...defaultOptions,
    ...options,
  };

  try {
    const data = $fetch<T>(url, mergedOptions);
    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

/** Get list of versions in a model
 * @param {string} token  api token to be used to make the request
 * @param {string} model  model to get the versions of
 * @returns {Array<string>} Sorted list of versions of the model
 */
export async function getModelVersions(
  token: string,
  model: string,
): Promise<Array<string>> {
  const data: Array<string> | null = await useApi(
    "/model/" + model + "/version",
    "GET",
    token,
  );
  return data?.sort() || [];
}

/**
 *
 */
export async function getVersionArtifacts(
  token: string,
  model: string,
  version: string,
): Promise<Array<ArtifactModel>> {
  const data: Array<ArtifactModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact",
    "GET",
    token,
  );
  return data || [];
}

// export async function getVersionReports(
//   token: string,
//   model: string,
//   version: string,
// ): Promise<Array<ReportModel>> {
//   const { data, error } = await useFetch<Array<ArtifactModel>>(
//     config.public.apiPath
//   )
// }

/**
 * Get report from API and return report response body
 */
export async function getReport(
  token: string,
  model: string,
  version: string,
  reportId: string,
): Promise<ReportModel> {
  const data: ArtifactModel | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + reportId,
    "GET",
    token,
  );
  if (data && data.body.artifact_type == "report") {
    return data.body;
  } else {
    return new ReportModel();
  }
}

/**
 *
 */
// export async function getTestSuite(
//   token: string,
//   model: string,
//   version: string,
//   testSuiteId: string,
// ): Promise {
//   const { data, error } = await useFetch<ArtifactModel>(
//     config.public.apiPath +
//       "/model/" +
//       model +
//       "/version/" +
//       version +
//       "/artifact/" +
//       testSuiteId,
//     {
//       retry: 0,
//       method: "GET",
//       headers: {
//         Authorization: "Bearer " + token,
//       },
//       onRequestError() {
//         requestErrorAlert();
//       },
//       onResponseError({ response }) {
//         handleHttpError(response.status, response._data.error_description);
//       },
//     },
//   );

//   if (
//     !error.value &&
//     data.value &&
//     data.value.body.artifact_type == "test_suite" &&
//     isValidTestSuite(data.value)
//   ) {
//     const testSuiteModel: TestSuiteModel = data.value.body;
//     return testSuiteModel;
//   } else {
//     return new ReportModel();
//   }
// }

/**
 *
 * @param artifactType
 * @param artifactName
 */
export function successfulSubmission(
  artifactType: string,
  artifactName: string,
  operation: string,
) {
  alert(
    `${artifactType}, ${artifactName}, has been ${operation} successfully.`,
  );
}
