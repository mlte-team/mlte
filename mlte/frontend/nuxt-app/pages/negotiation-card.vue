<template>
  <NuxtLayout name="base-layout">
    <title>Negotiation Card</title>
    <template #page-title>Negotiation Card</template>
    <template #right-sidebar>
      <div>
        TEC Import
        <hr />
        <div class="usa-form-group">
          <label class="usa-label"> System Context </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'System Context')"
          />

          <label class="usa-label"> Raw Data </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'Raw Data')"
          />

          <label class="usa-label"> Development Environment </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'Development Environment')"
          />

          <label class="usa-label"> Production Environment </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'Production Environment')"
          />
        </div>
      </div>
    </template>

    <p>
      Teams should use the negotiation card to guide an in-depth discussion for
      project scoping. The card can be completed in any order and the idea is
      that teams fill out as much as they can at the beginning of the project
      process and revisit the card throughout as the project matures. There are
      four sections in the Negotiation Card:
    </p>
    <ul>
      <li>System Information</li>
      <li>Data</li>
      <li>Model Information</li>
      <li>System Requirements</li>
    </ul>
    <p>
      Negotiation Cards serve as a critical reference for teams throughout
      development even when they are partially filled out. Hover over the black
      information icons next to each field to get more information about that
      field. Click on the Example button to see specific examples for a section.
    </p>

    <UsaTextInput
      v-if="queryArtifactId === undefined"
      v-model="userInputArtifactId"
      :error="formErrors.identifier"
    >
      <template #label>
        Artifact ID
        <InfoIcon>
          The Artifact ID this negotiation card <br />
          will be saved under upon submission.
        </InfoIcon>
      </template>
      <template #error-message> Identifier cannot be empty </template>
    </UsaTextInput>
    <div v-else>
      <h3 style="display: inline">Last Modified by:</h3>
      {{ creator }} - {{ timestamp }}
    </div>

    <FormFieldsSystemInformation
      ref="systemInformationRef"
      v-model="form.system"
    />

    <FormFieldsDataFields ref="dataRef" v-model="form.data" />

    <FormFieldsModelFields ref="modelRef" v-model="form.model" />

    <FormFieldsSystemRequirements v-model="form.system_requirements" />

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { cancelFormSubmission } from "~/composables/form-methods";

const config = useRuntimeConfig();
const token = useCookie("token");
const model = useRoute().query.model;
const version = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);

const userInputArtifactId = ref("");
const creator = ref("");
const timestamp = ref("");
const form = ref({
  artifact_type: "negotiation_card",
  system: new SystemDescriptor(),
  data: [new DataDescriptor()],
  model: new ModelDescriptor(),
  system_requirements: [new QASDescriptor()],
});

const formErrors = ref({
  identifier: false,
});

// References to child components used to call their methods when importing descriptors
const systemInformationRef = ref(null);
const dataRef = ref(null);
const modelRef = ref(null);

if (queryArtifactId !== undefined) {
  const { data: cardData, error } = await useFetch<NegotiationApiResponse>(
    config.public.apiPath +
      "/model/" +
      model +
      "/version/" +
      version +
      "/artifact/" +
      queryArtifactId,
    {
      retry: 0,
      method: "GET",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
  if (!error.value && cardData.value && isValidNegotiation(cardData.value)) {
    form.value = cardData.value.body;
    creator.value = cardData.value.header.creator;
    timestamp.value = new Date(
      cardData.value.header.timestamp * 1000,
    ).toLocaleString("en-US");
  }
}

async function submit() {
  const identifier = queryArtifactId || userInputArtifactId.value;
  if (identifier === "") {
    inputErrorAlert();
    return;
  }

  // Construct the object to be submitted to the backend here
  const artifact = {
    header: {
      identifier,
      type: "negotiation_card",
      timestamp: -1,
      creator: "",
    },
    body: form.value,
  };

  if (isValidNegotiation(artifact)) {
    try {
      await $fetch(
        config.public.apiPath +
          "/model/" +
          model +
          "/version/" +
          version +
          "/artifact",
        {
          retry: 0,
          method: "POST",
          headers: {
            Authorization: "Bearer " + token.value,
          },
          body: {
            artifact,
            force: forceSaveParam.value,
            parents: false,
          },
          onRequestError() {
            requestErrorAlert();
          },
          onResponse({ response }) {
            if (response.ok) {
              successfulArtifactSubmission("negotiation card", identifier);
              forceSaveParam.value = true;
              if (useRoute().query.artifactId === undefined) {
                window.location.href =
                  "/negotiation-card?" +
                  "model=" +
                  useRoute().query.model +
                  "&version=" +
                  useRoute().query.version +
                  "&artifactId=" +
                  identifier;
              }
            }
          },
          onResponseError({ response }) {
            handleHttpError(response.status, response._data.error_description);
          },
        },
      );
    } catch (exception) {
      console.log(exception);
    }
  } else {
    console.log("Invalid document attempting to be submitted.");
  }
}

function descriptorUpload(event: Event, descriptorName: string) {
  console.log(dataRef.value);

  const target = event.target as HTMLInputElement;
  const file = target.files![0];
  if (file !== null) {
    const reader = new FileReader();
    reader.onload = (inputFile) => {
      try {
        const document = JSON.parse((inputFile.target!.result as string) ?? "");
        if (descriptorName === "System Context") {
          document.goals.forEach(
            (goal: {
              id: string;
              goal: string;
              metric: string;
              baseline: string;
            }) => {
              let lastGoalIndex = form.value.system.goals.length - 1;
              if (!goalEmpty(form.value.system.goals[lastGoalIndex])) {
                // @ts-expect-error: TS18047 Reference to child component not expected functionality and has no type
                systemInformationRef.value.parentAddGoal();
                lastGoalIndex += 1;
              }

              form.value.system.goals[lastGoalIndex].description = goal.goal;
              form.value.system.goals[lastGoalIndex].metrics[0].description =
                goal.metric;
              form.value.system.goals[lastGoalIndex].metrics[0].baseline =
                goal.baseline;
            },
          );
          form.value.system.task = document.task;
          form.value.system.problem_type = document.ml_problem_type.ml_problem
            .toLowerCase()
            .split(" ")
            .join("_");
          form.value.system.usage_context = document.usage_context;
          form.value.system.risks.fp = document.risks.risk_fp;
          form.value.system.risks.fn = document.risks.risk_fn;
          form.value.system.risks.other = document.risks.risk_other;
        } else if (descriptorName === "Raw Data") {
          let lastDataIndex = form.value.data.length - 1;
          if (!dataItemEmpty(form.value.data[lastDataIndex])) {
            // @ts-expect-error: TS18047 Reference to child component not expected functionality and has no type
            dataRef.value.parentAddDataItem();
            lastDataIndex += 1;
          }

          let dataSourcesStr = "";
          document.data_sources.forEach(
            (
              source: { data_source: string; other_source: string },
              i: number,
            ) => {
              if (source.data_source === "Other") {
                dataSourcesStr += source.other_source;
              } else {
                dataSourcesStr += source.data_source;
              }

              if (i + 1 < document.data_sources.length) {
                dataSourcesStr += ", ";
              }
            },
          );
          form.value.data[lastDataIndex].source = dataSourcesStr;

          form.value.data[lastDataIndex].labels.splice(0, 1);
          document.labels_distribution.forEach(
            (label: { label: string; percentage: number }, i: number) => {
              // @ts-expect-error: TS18047 Reference to child component not expected functionality and has no type
              dataRef.value.parentAddLabel(lastDataIndex);
              form.value.data[lastDataIndex].labels[i].name = label.label;
              form.value.data[lastDataIndex].labels[i].percentage =
                label.percentage;
            },
          );

          form.value.data[lastDataIndex].rights = document.data_rights;
          form.value.data[lastDataIndex].policies = document.data_policies;
          form.value.data[lastDataIndex].description =
            document.dataset_description;

          form.value.data[lastDataIndex].fields.splice(0, 1);
          document.schema.forEach(
            (
              fields: {
                field_name: string;
                field_description: string;
                field_type: string;
                expected_values: string;
                interpret_missing: string;
                interpret_special: string;
              },
              i: number,
            ) => {
              // @ts-expect-error: TS18047 Reference to child component not expected functionality and has no type
              dataRef.value.parentAddField(lastDataIndex);
              form.value.data[lastDataIndex].fields[i].name = fields.field_name;
              form.value.data[lastDataIndex].fields[i].description =
                fields.field_description;
              form.value.data[lastDataIndex].fields[i].type = fields.field_type;
              form.value.data[lastDataIndex].fields[i].expected_values =
                fields.expected_values;
              form.value.data[lastDataIndex].fields[i].missing_values =
                fields.interpret_missing;
              form.value.data[lastDataIndex].fields[i].special_values =
                fields.interpret_special;
            },
          );
        } else if (descriptorName === "Development Environment") {
          form.value.model.development_compute_resources.gpu =
            document.computing_resources.gpu;
          form.value.model.development_compute_resources.cpu =
            document.computing_resources.cpu;
          form.value.model.development_compute_resources.memory =
            document.computing_resources.memory;
          form.value.model.development_compute_resources.storage =
            document.computing_resources.storage;

          document.upstream_components.forEach(
            (component: {
              component_name: string;
              output_spec: [
                {
                  item_name: string;
                  item_description: string;
                  item_type: string;
                  expected_values: string;
                },
              ];
              ml_component: boolean;
            }) => {
              component.output_spec.forEach((spec) => {
                let lastSpecIndex =
                  form.value.model.input_specification.length - 1;
                if (
                  !specEmpty(
                    form.value.model.input_specification[lastSpecIndex],
                  )
                ) {
                  // @ts-expect-error: TS18047 Reference to child component not expected functionality and has no type
                  modelRef.value.parentAddInputSpec();
                  lastSpecIndex += 1;
                }

                form.value.model.input_specification[lastSpecIndex] = {
                  name: component.component_name + "." + spec.item_name,
                  description: spec.item_description,
                  type: spec.item_type,
                  expected_values: spec.expected_values,
                };
              });
            },
          );

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
              component.input_spec.forEach((spec) => {
                let lastSpecIndex =
                  form.value.model.output_specification.length - 1;
                if (
                  !specEmpty(
                    form.value.model.output_specification[lastSpecIndex],
                  )
                ) {
                  // @ts-expect-error: TS18047 Reference to child component not expected functionality and has no type
                  modelRef.value.parentAddOutputSpec();
                  lastSpecIndex += 1;
                }

                form.value.model.output_specification[lastSpecIndex] = {
                  name: component.component_name + "." + spec.item_name,
                  description: spec.item_description,
                  type: spec.item_type,
                  expected_values: spec.expected_values,
                };
              });
            },
          );
        } else if (descriptorName === "Production Environment") {
          form.value.model.production_compute_resources.gpu =
            document.computing_resources.gpu;
          form.value.model.production_compute_resources.cpu =
            document.computing_resources.cpu;
          form.value.model.production_compute_resources.memory =
            document.computing_resources.memory;
          form.value.model.production_compute_resources.storage =
            document.computing_resources.storage;
        }
      } catch (exception) {
        console.error("Invalid JSON or error in parsing file.");
        console.log(exception);
      }
    };
    reader.readAsText(file);
  }
}

function goalEmpty(goal: GoalDescriptor) {
  let isEmpty = true;

  if (goal.description !== "") {
    isEmpty = false;
  }

  goal.metrics.forEach((metric: MetricDescriptor) => {
    if (metric.description !== "" || metric.baseline !== "") {
      isEmpty = false;
    }
  });

  return isEmpty;
}

function dataItemEmpty(dataItem: DataDescriptor) {
  let isEmpty = true;

  if (
    dataItem.description !== "" ||
    dataItem.source !== "" ||
    dataItem.classification !== "unclassified" ||
    dataItem.access !== "" ||
    dataItem.labeling_method !== ""
  ) {
    isEmpty = false;
  }

  dataItem.labels.forEach((label: LabelDescriptor) => {
    if (
      label.name !== "" ||
      label.description !== "" ||
      label.percentage !== 0
    ) {
      isEmpty = false;
    }
  });

  dataItem.fields.forEach((field: FieldDescriptor) => {
    if (
      field.name !== "" ||
      field.description !== "" ||
      field.type !== "" ||
      field.expected_values !== "" ||
      field.missing_values !== "" ||
      field.special_values !== ""
    ) {
      isEmpty = false;
    }
  });

  return isEmpty;
}

function specEmpty(spec: ModelIODescriptor) {
  let isEmpty = true;

  if (
    spec.name !== "" ||
    spec.description !== "" ||
    spec.type !== "" ||
    spec.expected_values !== ""
  ) {
    isEmpty = false;
  }

  return isEmpty;
}
</script>
