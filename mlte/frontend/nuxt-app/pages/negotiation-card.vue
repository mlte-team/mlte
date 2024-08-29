<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 255px">
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

    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">Negotiation Card</h1>
    <p>
      Teams should use the negotiation card to guide an in-depth 
      discussion for project scoping. The card can be completed in 
      any order and the idea is that teams fill out as much as they 
      can at the beginning of the project process and revisit the card 
      throughout as the project matures. There are four sections in 
      the Negotiation Card:
      <ul>
        <li>System Information</li>
        <li>Data</li>
        <li>Model Information</li>
        <li>System Requirements</li>
      </ul>
      Negotiation Cards serve as a critical reference for teams 
      throughout development even when they are partially filled out. 
      Hover over the black information icons next to each field to 
      get more information about that field. Click on the Example 
      button to see specific examples for a section.
    </p>

    <UsaTextInput
      v-if="useRoute().query.artifactId === undefined"
      v-model="userInputArtifactId"
    >
      <template #label>
        Artifact ID
        <InfoIcon>
          The Artifact ID this negotiation card <br />
          will be saved under upon submission.
        </InfoIcon>
      </template>
    </UsaTextInput>
    <div v-else>
      <h3>Last Modified by:</h3>
      {{ creator }} - {{ timestamp }}
    </div>

    <FormFieldsSystemInformation ref="systemInformationRef" v-model="form.nc_data.system"/>

    <FormFieldsDataFields ref="dataRef" v-model="form.nc_data.data"/>

    <FormFieldsModelFields ref="modelRef" v-model="form.nc_data.model"/>

    <FormFieldsSystemRequirements v-model="form.nc_data.system_requirements" />

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/here",
    text: "Negotiation Card",
  },
]);

const userInputArtifactId = ref("");
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);

const creator = ref("");
const timestamp = ref("");
const form = ref({
  artifact_type: "negotiation_card",
  nc_data: {
    system: {
      goals: [
        {
          description: "",
          metrics: [
            {
              description: "",
              baseline: "",
            },
          ],
        },
      ],
      problem_type: "classification",
      task: "",
      usage_context: "",
      risks: {
        fp: "",
        fn: "",
        other: "",
      },
    },
    data: [
      {
        description: "",
        source: "",
        classification: "unclassified",
        access: "",
        labeling_method: "",
        labels: [
          {
            name: "",
            description: "",
            percentage: 0,
          },
        ],
        fields: [
          {
            name: "",
            description: "",
            type: "",
            expected_values: "",
            missing_values: "",
            special_values: "",
          },
        ],
        rights: "",
        policies: "",
      },
    ],
    model: {
      development_compute_resources: {
        gpu: "0",
        cpu: "0",
        memory: "0",
        storage: "0",
      },
      deployment_platform: "",
      capability_deployment_mechanism: "",
      input_specification: [
        {
          name: "",
          description: "",
          type: "",
          expected_values: "",
        },
      ],
      output_specification: [
        {
          name: "",
          description: "",
          type: "",
          expected_values: "",
        },
      ],
      production_compute_resources: {
        gpu: "0",
        cpu: "0",
        memory: "0",
        storage: "0",
      },
    },
    system_requirements: [
      {
        quality: "<System Quality>",
        stimulus: "<Stimulus>",
        source: "<Source>",
        environment: "<Environment>",
        response: "<Response>",
        measure: "<Response Measure>",
      },
    ],
  },
});

const classificationOptions = useClassificationOptions();
const problemTypeOptions = useProblemTypeOptions();

const systemInformationRef = ref(null);
const dataRef = ref(null);
const modelRef = ref(null);

if (useRoute().query.artifactId !== undefined) {
  const model = useRoute().query.model;
  const version = useRoute().query.version;
  const artifactId = useRoute().query.artifactId;

  await useFetch(
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
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (isValidNegotiation(response._data)) {
          creator.value = response._data.header.creator;
          timestamp.value = new Date(
            response._data.header.timestamp * 1000,
          ).toLocaleString("en-US");
          form.value = response._data.body;

          const problemType = response._data.body.nc_data.system.problem_type;
          if (
            problemTypeOptions.value.find((x) => x.value === problemType)?.value !==
            undefined
          ) {
            form.value.nc_data.system.problem_type = problemTypeOptions.value.find(
              (x) => x.value === problemType,
            )?.value;
          }

          response._data.body.nc_data.data.forEach((item) => {
            const classification = item.classification;
            if (
              classificationOptions.value.find((x) => x.value === classification)
                ?.value !== undefined
            ) {
              item.classification = classificationOptions.value.find(
                (x) => x.value === classification,
              )?.value;
            }
          });
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
}

async function submit() {
  const model = useRoute().query.model;
  const version = useRoute().query.version;

  let identifier = "";
  if (useRoute().query.artifactId === undefined) {
    identifier = userInputArtifactId.value;
  } else {
    identifier = useRoute().query.artifactId?.toString();
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
          onResponseError({ response }) {
            handleHttpError(response.status, response._data.error_description);
          },
        },
      );
      successfulArtifactSubmission("negotiation card", identifier);
      forceSaveParam.value = true;
    } catch {}
  } else {
    console.log("Invalid document attempting to be submitted.");
  }
}

function descriptorUpload(event: Event, descriptorName: string) {
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
              let lastGoalIndex = form.value.nc_data.system.goals.length - 1;
              if (!goalEmpty(form.value.nc_data.system.goals[lastGoalIndex])) {
                systemInformationRef.value.parentAddGoal();
                lastGoalIndex += 1;
              }

              form.value.nc_data.system.goals[lastGoalIndex].description =
                goal.goal;
              form.value.nc_data.system.goals[
                lastGoalIndex
              ].metrics[0].description = goal.metric;
              form.value.nc_data.system.goals[
                lastGoalIndex
              ].metrics[0].baseline = goal.baseline;
            },
          );
          form.value.nc_data.system.task = document.task;
          form.value.nc_data.system.problem_type =
            document.ml_problem_type.ml_problem
              .toLowerCase()
              .split(" ")
              .join("_");
          form.value.nc_data.system.usage_context = document.usage_context;
          form.value.nc_data.system.risks.fp = document.risks.risk_fp;
          form.value.nc_data.system.risks.fn = document.risks.risk_fn;
          form.value.nc_data.system.risks.other = document.risks.risk_other;
        } else if (descriptorName === "Raw Data") {
          let lastDataIndex = form.value.nc_data.data.length - 1;
          if (!dataItemEmpty(form.value.nc_data.data[lastDataIndex])) {
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
          form.value.nc_data.data[lastDataIndex].source = dataSourcesStr;

          form.value.nc_data.data[lastDataIndex].labels.splice(0, 1);
          document.labels_distribution.forEach(
            (label: { label: string; percentage: number }, i: number) => {
              dataRef.value.parentAddLabel(lastDataIndex);
              form.value.nc_data.data[lastDataIndex].labels[i].name =
                label.label;
              form.value.nc_data.data[lastDataIndex].labels[i].percentage =
                label.percentage;
            },
          );

          form.value.nc_data.data[lastDataIndex].rights = document.data_rights;
          form.value.nc_data.data[lastDataIndex].policies =
            document.data_policies;
          form.value.nc_data.data[lastDataIndex].description =
            document.dataset_description;

          form.value.nc_data.data[lastDataIndex].fields.splice(0, 1);
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
              dataRef.value.parentAddField(lastDataIndex);
              form.value.nc_data.data[lastDataIndex].fields[i].name =
                fields.field_name;
              form.value.nc_data.data[lastDataIndex].fields[i].description =
                fields.field_description;
              form.value.nc_data.data[lastDataIndex].fields[i].type =
                fields.field_type;
              form.value.nc_data.data[lastDataIndex].fields[i].expected_values =
                fields.expected_values;
              form.value.nc_data.data[lastDataIndex].fields[i].missing_values =
                fields.interpret_missing;
              form.value.nc_data.data[lastDataIndex].fields[i].special_values =
                fields.interpret_special;
            },
          );
        } else if (descriptorName === "Development Environment") {
          form.value.nc_data.model.development_compute_resources.gpu =
            document.computing_resources.gpu;
          form.value.nc_data.model.development_compute_resources.cpu =
            document.computing_resources.cpu;
          form.value.nc_data.model.development_compute_resources.memory =
            document.computing_resources.memory;
          form.value.nc_data.model.development_compute_resources.storage =
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
                  form.value.nc_data.model.input_specification.length - 1;
                if (
                  !specEmpty(
                    form.value.nc_data.model.input_specification[lastSpecIndex],
                  )
                ) {
                  modelRef.value.parentAddInputSpec();
                  lastSpecIndex += 1;
                }

                form.value.nc_data.model.input_specification[lastSpecIndex] = {
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
                  form.value.nc_data.model.output_specification.length - 1;
                if (
                  !specEmpty(
                    form.value.nc_data.model.output_specification[
                      lastSpecIndex
                    ],
                  )
                ) {
                  modelRef.value.parentAddOutputSpec();
                  lastSpecIndex += 1;
                }

                form.value.nc_data.model.output_specification[lastSpecIndex] = {
                  name: component.component_name + "." + spec.item_name,
                  description: spec.item_description,
                  type: spec.item_type,
                  expected_values: spec.expected_values,
                };
              });
            },
          );
        } else if (descriptorName === "Production Environment") {
          form.value.nc_data.model.production_compute_resources.gpu =
            document.computing_resources.gpu;
          form.value.nc_data.model.production_compute_resources.cpu =
            document.computing_resources.cpu;
          form.value.nc_data.model.production_compute_resources.memory =
            document.computing_resources.memory;
          form.value.nc_data.model.production_compute_resources.storage =
            document.computing_resources.storage;
        }
      } catch (err) {
        console.error("Invalid JSON or error in parsing file.");
        console.log(err);
      }
    };
    reader.readAsText(file);
  }
}

function goalEmpty(goal) {
  let isEmpty = true;

  if (goal.description !== "") {
    isEmpty = false;
  }

  goal.metrics.forEach((metric) => {
    if (metric.description !== "" || metric.baseline !== "") {
      isEmpty = false;
    }
  });

  return isEmpty;
}

function dataItemEmpty(dataItem) {
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

  dataItem.labels.forEach((label) => {
    if (
      label.name !== "" ||
      label.description !== "" ||
      label.percentage !== 0
    ) {
      isEmpty = false;
    }
  });

  dataItem.fields.forEach((field) => {
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

function specEmpty(spec) {
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
