import type { NitroFetchOptions } from "nitropack";

const config = useRuntimeConfig();

/**
 * Generic $fetch function for HTTP requests to API.
 *
 * @template T Expected type of the data returned from the API
 * @param {string} url URL to fetch data from
 * @param {string} method HTTP method to use for request
 * @param {NitroFetchOptions<string>} [options] Optional configuration for $fetch
 * @param {string} [tokenOverride] Token provided to authenticate with API instead of cookie. Used in cases
 *                                  where token is set and then needs to be used immediately for a request.
 *                                  In theory, should only be needed if SSR is enabled but cookie is unable
 *                                  to be retrieved if this is not passed in these cases
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

// --------------------------------------------------------------------------------------------------------------
// Context
// --------------------------------------------------------------------------------------------------------------

/**
 * Get sorted list of Versions in a Model.
 *
 * @param {string} model Model to get the Versions of
 * @returns {Array<string>} Sorted list of Versions of the Model
 */
export async function getModelVersions(model: string): Promise<Array<string>> {
  const versions: Array<string> | null = await useApi(
    "/model/" + model + "/version",
    "GET",
  );
  return versions?.sort() || [];
}

// --------------------------------------------------------------------------------------------------------------
// Group
// --------------------------------------------------------------------------------------------------------------

/**
 * 
 */
export async function getPermissionList(): Promise<Array<Permission>> {
  const permissionList: Array<Permission> | null = await useApi(
    "/groups/permissions/details",
    "GET",
  );
  return permissionList || [];
}

// --------------------------------------------------------------------------------------------------------------
// Artifact
// --------------------------------------------------------------------------------------------------------------

/**
 * Get Negotiation Card from API.
 *
 * @param {string} model Model of the Version
 * @param {string} version Version of the Negotiation Card
 * @returns {Promise<NegotiationCardModel>} Promise that resolves to Negotiation Card
 */
export async function getCard(
  model: string,
  version: string,
  cardId: string,
): Promise<ArtifactModel<NegotiationCardModel> | null> {
  const card: ArtifactModel<NegotiationCardModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + cardId,
    "GET",
  );
  if (card && card.body.artifact_type == "negotiation_card") {
    return card;
  } else {
    return null;
  }
}

/**
 * Get report from API.
 *
 * @param {string} model Model of the version
 * @param {string} version Version of the report
 * @returns {Promise<ReportModel>} Promise that resolves to report
 */
export async function getReport(
  model: string,
  version: string,
  reportId: string,
): Promise<ArtifactModel<ReportModel> | null> {
  const report: ArtifactModel<ReportModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + reportId,
    "GET",
  );
  if (report && report.body.artifact_type == "report") {
    return report;
  } else {
    return null;
  }
}

// --------------------------------------------------------------------------------------------------------------
// Util
// --------------------------------------------------------------------------------------------------------------

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
