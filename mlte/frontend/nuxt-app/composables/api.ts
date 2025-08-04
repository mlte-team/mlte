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
  options: NitroFetchOptions<string> | null = null,
  tokenOverride: string | null = null,
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
// Token
// --------------------------------------------------------------------------------------------------------------

export async function getToken(
  username: string,
  password: string,
): Promise<TokenData | null> {
  const details: Dictionary<string> = {
    grant_type: "password",
    username: username,
    password: password,
  };

  const formBodyArray: Array<string> = [];
  for (const property in details) {
    const encodedKey = encodeURIComponent(property);
    const encodedValue = encodeURIComponent(details[property]);
    formBodyArray.push(encodedKey + "=" + encodedValue);
  }
  const formBodyStr: string = formBodyArray.join("&");

  const tokenData: TokenData | null = await useApi(
    "/token",
    "POST",
    {
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formBodyStr,
    },
    undefined,
    false,
  );
  return tokenData;
}

// --------------------------------------------------------------------------------------------------------------
// Context
// --------------------------------------------------------------------------------------------------------------

/**
 * Create new Model with API.
 *
 * @param {string} modelName Name of model to be created
 * @returns {Promise<Model | null>} Promise that resolves to crated Model or null on failure
 */
export async function createModel(modelName: string): Promise<Model | null> {
  const response: Model | null = await useApi("/model/", "POST", {
    body: { identifier: modelName },
  });
  return response;
}

/**
 * Create new Version with API.
 *
 * @param {string} modelName Name of model
 * @param {string} versionName Name of Version to be created
 * @returns {Promise<Model | null>} Promise that resolves to crated Version or null on failure
 */
export async function createVersion(
  modelName: string,
  versionName: string,
): Promise<Version | null> {
  const response: Version | null = await useApi(
    "/model/" + modelName + "/version",
    "POST",
    {
      body: { identifier: versionName },
    },
  );
  return response;
}

/**
 * Get sorted list of Versions in a Model from API.
 *
 * @param {string} model Model to get the Versions of
 * @returns {Array<string>} Promise that resolves to sorted list of Versions of the Model
 */
export async function getModelVersions(model: string): Promise<Array<string>> {
  const versions: Array<string> | null = await useApi(
    "/model/" + model + "/version",
    "GET",
  );
  return versions?.sort() || [];
}

// --------------------------------------------------------------------------------------------------------------
// User
// --------------------------------------------------------------------------------------------------------------

export async function getUserMe(token: string){
  const user: User | null = await useApi(
    "/user/me",
    "GET",
    undefined,
    token as string,
  );
  return user;
}

/**
 * Get sorted list of Models available to User from API.
 *
 * @return {Promise<Array<string>>} Promise that resolves to sorted list of Models available to User
 */
export async function getUserModels(): Promise<Array<string>> {
  const models: Array<string> | null = await useApi("/user/me/models", "GET");
  return models?.sort() || [];
}

// --------------------------------------------------------------------------------------------------------------
// Group
// --------------------------------------------------------------------------------------------------------------

/**
 * Get list of Groups from API.
 *
 * @return {Promise<Array<Group>>} Promise that resolves to list of Groups
 */
export async function getGroupList(): Promise<Array<Group>> {
  const groupList: Array<Group> | null = await useApi("/groups/details", "GET");
  return groupList || [];
}

/**
 * Get list of Permissions from API.
 *
 * @returns {Promise<Array<Permission>>} Promise that resolves to list of Permissions
 */
export async function getPermissionList(): Promise<Array<Permission>> {
  const permissionList: Array<Permission> | null = await useApi(
    "/groups/permissions/details",
    "GET",
  );
  return permissionList || [];
}

// --------------------------------------------------------------------------------------------------------------
// Test Catalog
// --------------------------------------------------------------------------------------------------------------

/**
 * Get list of Catalogs from API.
 *
 * @return {Promise<Array<CatalogReply>>} Promise that resolves to list of Catalogs
 */
export async function getCatalogList(): Promise<Array<CatalogReply>> {
  const catalogList: Array<CatalogReply> | null = await useApi(
    "/catalogs",
    "GET",
  );
  return catalogList || [];
}

/**
 * Perform a search for Test Catalog Entries with API.
 *
 * @param {object} filter Filter object to be sent with request
 * @return {Promise<Array<TestCatalogEntry>>} Promise that resolves to list of Test Catalog Entries meeting search criteria
 */
export async function searchCatalog(
  filter: object,
): Promise<Array<TestCatalogEntry>> {
  const catalogList: Array<TestCatalogEntry> | null = await useApi(
    "/catalogs/entry/search",
    "POST",
    { body: filter },
  );
  return catalogList || [];
}

/**
 * Create new Test Catalog Entry with API.
 *
 * @param {string} catalogId ID of Test Catalog to add entry to
 * @param {TestCatalogEntry} entry Test Catalog Entry to create
 * @returns {Promise<TestCatalogEntry | null>} Promise that resolves to created Test Catalog Entry, or null on a failure
 */
export async function createCatalogEntry(
  catalogId: string,
  entry: TestCatalogEntry,
): Promise<TestCatalogEntry | null> {
  const response: TestCatalogEntry | null = await useApi(
    "/catalog/" + catalogId + "/entry",
    "POST",
    {
      body: JSON.stringify(entry),
    },
  );
  return response;
}

/**
 * Update Test Catalog Entry with API.
 *
 * @param {string} catalogId ID of Test Catalog containing entry to update
 * @param {TestCatalogEntry} entry Test Catalog Entry to update
 * @returns {Promise<TestCatalogEntry | null>} Updated Test Catalog Entry, or null on a failure
 */
export async function updateCatalogEntry(
  catalogId: string,
  entry: TestCatalogEntry,
): Promise<TestCatalogEntry | null> {
  const response: TestCatalogEntry | null = await useApi(
    "catalog/" + catalogId + "/entry",
    "PUT",
    { body: JSON.stringify(entry) },
  );
  return response;
}

/**
 * Delete a Test Catalog Entry with API.
 *
 * @param {string} catalogId ID of Test Catalog containing entry to be deleted
 * @param {string} entryId ID of the Test Catalog Entry to be deleted
 * @return {Promise<TestCatalogEntry | null>} Promise that resolves to deleted Test Catalog Entry, or null on a failure
 */
export async function deleteCatalogEntry(
  catalogId: string,
  entryId: string,
): Promise<TestCatalogEntry | null> {
  const deletedEntry: TestCatalogEntry | null = await useApi(
    "/catalog/" + catalogId + "/entry/" + entryId,
    "DELETE",
  );
  return deletedEntry;
}

// --------------------------------------------------------------------------------------------------------------
// Artifact
// --------------------------------------------------------------------------------------------------------------

/**
 * Get all Artifacts of a Model Version.
 *
 * @param {string} model Model of the Version
 * @param {string} version Version of the Artifacts
 * @returns {Promise<Array<ArtifactModel>>} Promise that resolves to list of Artifacts
 */
export async function getVersionArtifacts(
  model: string,
  version: string,
): Promise<Array<ArtifactModel>> {
  const versionArtifacts: Array<ArtifactModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact",
    "GET",
  );
  return versionArtifacts || [];
}

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
 * Get Report from API.
 *
 * @param {string} model Model of the version
 * @param {string} version Version of the Report
 * @returns {Promise<ReportModel>} Promise that resolves to Report
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
// Custom List
// --------------------------------------------------------------------------------------------------------------

/**
 * Get Custom List from API.
 *
 * @param {string} customListId ID of the custom list
 * @returns {Promise<Array<CustomListEntry>>} Promise that resolves to Custom List
 */
export async function getCustomList(
  customListId: string,
): Promise<Array<CustomListEntry>> {
  const customList: Array<CustomListEntry> | null = await useApi(
    "/custom_list/" + customListId,
    "GET",
  );
  return customList || [];
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
