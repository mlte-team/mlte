import type { Dictionary } from "../composables/types";

const config = useRuntimeConfig();

export function resetFormErrors(
  formErrors: Dictionary<boolean>,
): Dictionary<boolean> {
  for (const key in formErrors) {
    formErrors[key] = false;
  }

  return formErrors;
}

// Fetch a artifact by ID.
export async function fetchArtifact(
  token: string,
  model: string,
  version: string,
  artifactId: string,
): Promise<Artifact> {
  const data: Artifact = await $fetch(
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
      onResponse({ response }) {
        return response._data;
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );

  return data;
}
