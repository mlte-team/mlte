<script setup lang="ts">
const config = useRuntimeConfig();

// TODO(Kyle): Add this functionality back. Decide where in the UI it should go.
async function deleteModel(entry: { model: string; selected: boolean }) {
  if (
    confirm("Are you sure you want to delete the model: " + entry.model + "?")
  ) {
    await useFetch(
      config.public.apiPath + 
        "/model/" +
        entry.model,
      {
        retry: 0,
        method: "DELETE",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse() {
          const index = modelOptions.value.indexOf(entry);
          modelOptions.value.splice(index, 1);
          updateSelectedModels(entry);
          negotiationCards.value = [];
          reports.value = [];
          specifications.value = [];
          validatedSpecs.value = [];
          values.value = [];
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
}

// TODO(Kyle): Add this functionality back. Decide where in the UI it should go.
async function deleteVersion(entry: {
  model: string;
  version: string;
  selected: boolean;
}) {
  if (
    confirm(
      "Are you sure you want to delete the version: " +
        entry.model +
        " - " +
        entry.version +
        "?",
    )
  ) {
    await useFetch(
      config.public.apiPath + 
        "/model/" +
        entry.model +
        "/version/" +
        entry.version,
      {
        retry: 0,
        method: "DELETE",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse() {
          const index = versionOptions.value.indexOf(entry);
          versionOptions.value.splice(index, 1);
          clearDeselectedArtifacts(entry.model, entry.version);
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
}
</script>
