// Fetch a artifact by ID.
export async function fetchArtifact(
  namespace: string,
  model: string,
  version: string,
  artifactId: string,
) {
  const data = await $fetch(
    "http://localhost:8080/api/namespace/" +
      namespace +
      "/model/" +
      model +
      "/version/" +
      version +
      "/artifact/" +
      artifactId,
    {
      retry: 0,
      method: "GET",
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        return response._data;
      },
      onResponseError() {
        responseErrorAlert();
      },
    },
  );

  return data;
}