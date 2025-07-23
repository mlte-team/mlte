import type { NitroFetchOptions } from "nitropack";

const config = useRuntimeConfig();

/**
 * Generic $fetch function for HTTP requests to API.
 *
 * @template T Expected type of the data returned from the API
 * @param {string} url URL to fetch data from
 * @param {string} method HTTP method to use for request
 * @param {NitroFetchOptions<string>} [options] Optional configuration for $fetch
 * @param {string} [tokenOverride] Token provided to authenticate with API instead of cookie
 * @param {boolean} [auth] Flag to add token to request or not. Default true
 * @returns {Promise<T> | null} Promise that resolves to the data from request or null if there is an error
 */
export function useApi<T>(
  url: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  options?: NitroFetchOptions<string>,
  tokenOverride?: string,
  auth: boolean = true,
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

  if (auth) {
    if (tokenOverride) {
      defaultOptions["headers"] = { Authorization: "Bearer " + tokenOverride };
    } else {
      const token = useCookie("token");
      defaultOptions["headers"] = { Authorization: "Bearer " + token.value };
    }
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

/**
 * Get sorted list of versions in a model.
 *
 * @param {string} model Model to get the versions of
 * @returns {Array<string>} Sorted list of versions of the model
 */
export async function getModelVersions(model: string): Promise<Array<string>> {
  const data: Array<string> | null = await useApi(
    "/model/" + model + "/version",
    "GET",
  );
  return data?.sort() || [];
}

/**
 * Get report from API and return report response body.
 *
 * @param {string} model Model containing the version
 * @param {string} version Version containing the report
 * @returns {Promise<ReportModel>} Promise that resolves to report
 */
export async function getReport(
  model: string,
  version: string,
  reportId: string,
): Promise<ReportModel> {
  const data: ArtifactModel | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + reportId,
    "GET",
  );
  if (data && data.body.artifact_type == "report") {
    return data.body;
  } else {
    return new ReportModel();
  }
}

/**
 * Generic alert function for API interactions.
 *
 * @param {string} artifactType Type of artifact
 * @param {string} artifactName Name of artifact
 * @param {string} operation Name of operation performed
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
