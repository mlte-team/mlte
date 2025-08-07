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
  if (response) {
    successfulSubmission("Model", modelName, "created");
  }
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
  if (response) {
    successfulSubmission("Version", versionName, "created");
  }
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

export async function getUserMe(token: string = "") {
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
 * @returns {Promise<Array<string>>} Promise that resolves to sorted list of Models available to User
 */
export async function getUserModels(): Promise<Array<string>> {
  const models: Array<string> | null = await useApi("/user/me/models", "GET");
  return models?.sort() || [];
}

/**
 * Create User with API.
 *
 * @param {User} user User object to create
 * @returns {Promise<User | null>} Promise that resolves to created User or null on failure
 */
export async function createUser(user: User): Promise<User | null> {
  const response: User | null = await useApi("/user", "POST", {
    body: JSON.stringify(user),
  });
  if (response) {
    successfulSubmission("User", user.username, "created");
  }
  return response;
}

/**
 * Get all User details from API.
 *
 * @returns {Promise<Array<User> | null>} Promise that resolves to list of Users with details or null on failure
 */
export async function getUsersDetails(): Promise<Array<User> | null> {
  const users: Array<User> | null = await useApi("/users/details", "GET");
  return users;
}

/**
 * Update User with API.
 *
 * @param {User} user Updated version of the user
 * @returns {Promise<User | null>} Promise that resolves to updated User or null on failure
 */
export async function updateUser(user: User): Promise<User | null> {
  const response: User | null = await useApi("/user", "PUT", {
    body: JSON.stringify(user),
  });
  if (response) {
    successfulSubmission("User", user.username, "updated");
  }
  return response;
}

/**
 * Delete User with API.
 *
 * @param {string} username Username of the User to delete
 * @returns {Promise<User | null>} Promise that resolves to deleted User or null on failure
 */
export async function deleteUser(username: string): Promise<User | null> {
  const response: User | null = await useApi("/user/" + username, "DELETE");
  if (response) {
    successfulSubmission("User", username, "deleted");
  }
  return response;
}

// --------------------------------------------------------------------------------------------------------------
// Group
// --------------------------------------------------------------------------------------------------------------

/**
 * Create Group with API.
 *
 * @param {Group} group Group to be create
 * @returns {Promise<Group | null>} Promise that resolves to created Group or null on failure
 */
export async function createGroup(group: Group): Promise<Group | null> {
  const response: Group | null = await useApi("/group", "POST", {
    body: JSON.stringify(group),
  });
  if (response) {
    successfulSubmission("Group", group.name, "created");
  }
  return response;
}

/**
 * Get list of Groups from API.
 *
 * @returns {Promise<Array<Group>>} Promise that resolves to list of Groups
 */
export async function getGroupList(): Promise<Array<Group>> {
  const groupList: Array<Group> | null = await useApi("/groups/details", "GET");
  return groupList || [];
}

/**
 * Update Group with API.
 *
 * @param {Group} group Updated version of Group
 * @returns {Promise<Group | null>} Promise that resolves to updated Group or null on failure
 */
export async function updateGroup(group: Group): Promise<Group | null> {
  const response: Group | null = await useApi("/group", "PUT", {
    body: JSON.stringify(group),
  });
  if (response) {
    successfulSubmission("Group", group.name, "updated");
  }
  return response;
}

/**
 * Delete Group with API
 *
 * @param {string} groupName Name of Group to be deleted
 * @returns {Promise<Group | null>} Promise that resolves to deleted Group or null on failure
 */
export async function deleteGroup(groupName: string): Promise<Group | null> {
  const group: Group | null = await useApi("/group/" + groupName, "DELETE");
  if (group) {
    successfulSubmission("Group", groupName, "deleted");
  }
  return group;
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
 * @returns {Promise<Array<CatalogReply>>} Promise that resolves to list of Catalogs
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
 * @returns {Promise<Array<TestCatalogEntry>>} Promise that resolves to list of Test Catalog Entries meeting search criteria
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
  if (response) {
    successfulSubmission(
      "Test Catalog Entry",
      entry.header.identifier,
      "created",
    );
  }
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
  if (response) {
    successfulSubmission(
      "Test Catalog Entry",
      entry.header.identifier,
      "updated",
    );
  }
  return response;
}

/**
 * Delete a Test Catalog Entry with API.
 *
 * @param {string} catalogId ID of Test Catalog containing entry to be deleted
 * @param {string} entryId ID of the Test Catalog Entry to be deleted
 * @returns {Promise<TestCatalogEntry | null>} Promise that resolves to deleted Test Catalog Entry, or null on a failure
 */
export async function deleteCatalogEntry(
  catalogId: string,
  entryId: string,
): Promise<TestCatalogEntry | null> {
  const response: TestCatalogEntry | null = await useApi(
    "/catalog/" + catalogId + "/entry/" + entryId,
    "DELETE",
  );
  if (response) {
    successfulSubmission("Test Catalog Entry", entryId, "deleted");
  }
  return response;
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
 * @returns {Promise<NegotiationCardModel>} Promise that resolves to the Negotiation Card
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
    if (isValidNegotiation(card)) {
      return card;
    } else {
      invalidArtifactAlert(
        "Negotiation card",
        card.header.identifier,
        "loaded",
      );
    }
  }
  return null;
}

/**
 * Save a Negotiation Card with API.
 *
 * @param {string} model Model of the Version
 * @param {string} version Version to contain the Negotiation Card
 * @param {string} identifier Identifier for the Negotiation Card
 * @param {boolean} forceSave Force save true incidates an update to a Negotiatoin Card, false indates a new Negotation Card
 * @param {NegotiationCardModel} card Negotiation Card to be saved
 * @returns {Promise<NegotiationCardModel | null>} Promise that resolves to saved Negotiation Card or null on failure
 */
export async function saveCard(
  model: string,
  version: string,
  identifier: string,
  forceSave: boolean,
  card: NegotiationCardModel,
): Promise<NegotiationCardModel | null> {
  // Construct the object to be submitted to the backend
  const artifact = {
    header: {
      identifier,
      type: "negotiation_card",
      timestamp: -1,
      creator: "",
    },
    body: card,
  };

  if (isValidNegotiation(artifact)) {
    const response: NegotiationCardModel | null = await useApi(
      "/model/" + model + "/version/" + version + "/artifact",
      "POST",
      { body: { artifact, force: forceSave, parents: false } },
    );
    if (response) {
      successfulSubmission("Negotiation card", identifier, "saved");
      return response;
    }
  } else {
    invalidArtifactAlert("Negotiation card", identifier, "saved");
  }
  return null;
}

/**
 * Get Report from API.
 *
 * @param {string} model Model of the Version
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
    if (isValidReport(report)) {
      return report;
    } else {
      invalidArtifactAlert("Report", report.header.identifier, "loaded");
    }
  }
  return null;
}

/**
 * Get Test Suite from API.
 *
 * @param {string} model Model of the Version
 * @param {string} version Version of the Test Suite
 * @returns {Promise<TestSuiteModel>} Promise that resolves to the Test Suite
 */
export async function getSuite(
  model: string,
  version: string,
  suiteId: string,
): Promise<ArtifactModel<TestSuiteModel> | null> {
  const suite: ArtifactModel<TestSuiteModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + suiteId,
    "GET",
  );
  if (suite && suite.body.artifact_type == "test_suite") {
    return suite;
  } else {
    return null;
  }
}

/**
 * Get Test Results from API.
 *
 * @param {string} model Model of the Version
 * @param {string} version Version of the Test Results
 * @returns {Promise<TestResultsModel>} Promise that resolves to the Test Results
 */
export async function getResults(
  model: string,
  version: string,
  suiteId: string,
): Promise<ArtifactModel<TestResultsModel> | null> {
  const results: ArtifactModel<TestResultsModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + suiteId,
    "GET",
  );
  if (results && results.body.artifact_type == "test_results") {
    return results;
  } else {
    return null;
  }
}

/**
 * Get Evidence from API.
 *
 * @param {string} model Model of the Version
 * @param {string} version Version of the Evidence
 * @returns {Promise<EvidenceModel>} Promise that resolves to the Evidence
 */
export async function getEvidence(
  model: string,
  version: string,
  suiteId: string,
): Promise<ArtifactModel<EvidenceModel> | null> {
  const evidence: ArtifactModel<EvidenceModel> | null = await useApi(
    "/model/" + model + "/version/" + version + "/artifact/" + suiteId,
    "GET",
  );
  if (evidence && evidence.body.artifact_type == "evidence") {
    return evidence;
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
 * Generic alert function for successful API interactions.
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

/**
 *
 */
export function invalidArtifactAlert(
  artifactType: string,
  artifactName: string,
  operation: string,
) {
  alert(
    `${artifactType}, ${artifactName}, is invalid and cannot be ${operation} successfully.`,
  );
}
