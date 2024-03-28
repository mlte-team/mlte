const config = useRuntimeConfig();

// Fetch a artifact by ID.
export async function fetchArtifact(
  token: string,
  model: string,
  version: string,
  artifactId: string,
) {
  const data = await $fetch(
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
        'Authorization': 'Bearer ' + token
      },
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
