<script setup lang="ts">
// TODO(Kyle): Add this functionality back. Decide where in the UI it should go.
async function deleteModel(entry: { model: string; selected: boolean }) {
  if (
    confirm("Are you sure you want to delete the model: " + entry.model + "?")
  ) {
    await useFetch(
      "http://localhost:8080/api/namespace/" +
        selectedNamespace.value +
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
      "http://localhost:8080/api/namespace/" +
        selectedNamespace.value +
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

// TODO(Kyle): I do not think we need this anymore.
function clearDeselectedArtifacts(model: string, version: string) {
  // Passing a version causes both model and version to be checked before filtering items
  // If an empty string is passed as the version, all artifacts under the model will be filtered out

  negotiationCards.value = specifications.value.filter(function (card) {
    if (version === "") {
      return card.model !== model;
    } else {
      return card.model !== model || card.version !== version;
    }
  });

  reports.value = specifications.value.filter(function (report) {
    if (version === "") {
      return report.model !== model;
    } else {
      return report.model !== model || report.version !== version;
    }
  });

  specifications.value = specifications.value.filter(function (spec) {
    if (version === "") {
      return spec.model !== model;
    } else {
      return spec.model !== model || spec.version !== version;
    }
  });

  validatedSpecs.value = validatedSpecs.value.filter(function (validatedSpec) {
    if (version === "") {
      return validatedSpec.model !== model;
    } else {
      return validatedSpec.model !== model || validatedSpec.version !== version;
    }
  });

  values.value = values.value.filter(function (value) {
    if (version === "") {
      return value.model !== model;
    } else {
      return value.model !== model || value.version !== version;
    }
  });
}

// TODO(Kyle): What is this for?
function descriptorUpload(event: Event, descriptorName: string) {
  const target = event.target as HTMLInputElement;
  const file = target.files![0];
  if (file !== null) {
    const reader = new FileReader();
    reader.onload = (inputFile) => {
      try {
        const document = JSON.parse((inputFile.target!.result as string) ?? "");
        form.value.model_summary = document.model_summary;
        document.goals.forEach(
          (goal: {
            id: string;
            goal: string;
            metric: string;
            baseline: string;
          }) => {
            addGoal();
            const lastGoalIndex = form.value.goals.length - 1;

            form.value.goals[lastGoalIndex].description = goal.goal;
            form.value.goals[lastGoalIndex].metrics[0].description =
              goal.metric;
            form.value.goals[lastGoalIndex].metrics[0].baseline = goal.baseline;
          },
        );
        form.value.mlte_evaluation = document.mlte_evaluation;
        form.value.intended_use = document.intended_use;
        form.value.risks = document.risks;
        form.value.data = document.data;
        form.value.caveats = document.caveats;
        form.value.analysis = document.analysis;

        let outputString = "";

        document.downstream_components.forEach(
          (component: {
            component_name: string;
            input_spec: [
              {
                item_name: string;
                item_description: string;
                item_type: string;
                expected_values: string;
              },
            ];
            ml_component: boolean;
          }) => {
            outputString +=
              "Component Name: " + component.component_name + "\n";
            outputString += "ML Component: " + component.ml_component + "\n";
            component.input_spec.forEach(
              (spec: {
                item_name: string;
                item_description: string;
                item_type: string;
                expected_values: string;
              }) => {
                outputString += spec.item_name + "\n";
                outputString += spec.item_description + "\n";
                outputString += spec.item_type + "\n";
                outputString += spec.expected_values + "\n";
              },
            );
            outputString += "\n";
          },
        );
        outputString = outputString.substring(0, outputString.length - 2);
      } catch (err) {
        console.error("Invalid JSON or error in parsing file.");
      }
    };
    reader.readAsText(file);
  }
}
</script>
