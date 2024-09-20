<template>
  <NuxtLayout name="base-layout">
    <title>Report</title>
    <template #page-title>Report</template>
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

    <h2 class="section-header">Model Summary</h2>
    <p>A summary of the model under evaluation.</p>

    <UsaSelect
      v-model="form.nc_data.system.problem_type"
      :options="problemTypeOptions"
    >
      <template #label>
        Problem Type
        <InfoIcon> Type of ML problem the model is intended to solve </InfoIcon>
      </template>
    </UsaSelect>

    <UsaTextInput :model-value="form.nc_data.system.task">
      <template #label> Task </template>
    </UsaTextInput>

    <h2 class="section-header">Performance</h2>
    <p>Model performance evaluation.</p>
    <div class="input-group">
      <h3>Goals</h3>
      <p>Goals or objectives that the model is going to help satisfy.</p>
      <div
        v-for="(goal, goalIndex) in form.nc_data.system.goals"
        :key="goalIndex"
      >
        <h3>Goal {{ goalIndex + 1 }}</h3>

        <UsaTextInput v-model="goal.description">
          <template #label> Goal Description </template>
        </UsaTextInput>

        <h3 class="no-margin-sub-header">Metrics</h3>
        <div v-for="(metric, metricIndex) in goal.metrics" :key="metricIndex">
          <div class="inline-input-left">
            <UsaTextInput v-model="metric.description">
              <template #label>
                Description
                <InfoIcon>
                  For each goal, select a performance metric that captures the
                  system's <br />
                  ability to accomplish that goal; e.g., acceptance criteria for
                  determining <br />
                  that the model is performing correctly.
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-right">
            <UsaTextInput v-model="metric.baseline">
              <template #label>
                Baseline
                <InfoIcon>
                  Select a baseline for each performance metric, which means a
                  measurement that <br />
                  evaluates whether or not the model will/can achieve the main
                  goal for which it is being created. <br />
                  If the goal cannot be measured directly, select a reasonable
                  proxy and justify how that will <br />
                  reliably predict the model’s performance in achieving its
                  goal.
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>
          <div class="inline-button">
            <DeleteButton @click="deleteMetric(goalIndex, metricIndex)">
              Delete Metric
            </DeleteButton>
          </div>
        </div>
        <AddButton class="margin-button" @click="addMetric(goalIndex)">
          Add Metric
        </AddButton>
        <DeleteButton @click="deleteGoal(goalIndex)">
          Delete goal
        </DeleteButton>
        <hr />
      </div>

      <AddButton class="margin-button" @click="addGoal()"> Add goal </AddButton>
    </div>

    <h3>MLTE Evaluation</h3>
    <table class="table usa-table usa-table--borderless">
      <thead>
        <tr>
          <th data-sortable scope="col" role="columnheader">Status</th>
          <th data-sortable scope="col" role="columnheader">Property</th>
          <th data-sortable scope="col" role="columnheader">Measurement</th>
          <th data-sortable scope="col" role="columnheader">Evidence ID</th>
          <th data-sortable scope="col" role="columnheader">Message</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="finding in findings" :key="finding.evidence_id">
          <td
            v-if="finding.status == 'Success'"
            style="background-color: rgba(210, 232, 221, 255)"
          >
            {{ finding.status }}
          </td>
          <td
            v-else-if="finding.status == 'Ignore'"
            style="background-color: rgba(255, 243, 205, 255)"
          >
            {{ finding.status }}
          </td>
          <td
            v-else-if="finding.status == 'Failure'"
            style="background-color: rgba(248, 216, 219, 255)"
          >
            {{ finding.status }}
          </td>
          <td v-else>{{ finding.status }}</td>
          <td>{{ finding.property }}</td>
          <td>{{ finding.measurement }}</td>
          <td>{{ finding.evidence_id }}</td>
          <td>{{ finding.message }}</td>
        </tr>
      </tbody>
    </table>

    <h2 class="section-header">Intended Use</h2>
    <UsaTextarea
      v-model="form.nc_data.system.usage_context"
      style="margin-bottom: 1em"
    >
      <template #label>
        Usage Context for the Model
        <InfoIcon>
          Who is intended to utilize the system/model; how the results of the
          model are <br />
          going to be used by end users or in the context of a larger system.
          <br />
          <br />
          <i
            >Example: Model results are consumed by a system component that
            shows
            <br />
            an intel analyst a list of matching voice recordings.</i
          >
        </InfoIcon>
      </template>
    </UsaTextarea>

    <UsaTextarea v-model="form.nc_data.model.deployment_platform">
      <template #label>
        Deployment Platform
        <InfoIcon>
          Describe the deployment platform for the model, e.g., local server,
          <br />
          cloud server, embedded platform.
          <br />
          <br />
          <i>Example: Local server due to data classification issues.</i>
        </InfoIcon>
      </template>
    </UsaTextarea>

    <UsaTextarea v-model="form.nc_data.model.capability_deployment_mechanism">
      <template #label>
        Capability Deployment Mechanism
        <InfoIcon>
          Describe how the model capabilities will be made available, <br />
          e.g., API, user facing, data feed.
          <br />
          <br />
          <i
            >Example: The model will expose an API so that it can be called
            <br />
            from the intel analyst UI.</i
          >
        </InfoIcon>
      </template>
    </UsaTextarea>

    <FormFieldsInputSpecification
      v-model="form.nc_data.model.input_specification"
    />

    <FormFieldsOutputSpecification
      v-model="form.nc_data.model.output_specification"
    />

    <FormFieldsProductionCompute
      v-model="form.nc_data.model.production_compute_resources"
    />

    <h2 class="section-header">Risks</h2>
    <UsaTextInput v-model="form.nc_data.system.risks.fp">
      <template #label> False Positive Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.nc_data.system.risks.fn">
      <template #label> False Negative Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.nc_data.system.risks.other">
      <template #label> Other risks of producing incorrect results </template>
    </UsaTextInput>

    <h2 class="section-header">Data</h2>
    <p>A description of the data used to train the model.</p>

    <h2 class="section-header">Data</h2>
    <p>
      Details of the data that will influence development efforts; fill out all
      that are known. For access / availability, record what needs to happen to
      access the data, such as accounts that need to be created or methods for
      data transportation.
    </p>
    <div class="input-group">
      <div
        v-for="(dataItem, dataItemIndex) in form.nc_data.data"
        :key="dataItemIndex"
      >
        <h3>Data Item {{ dataItemIndex + 1 }}</h3>
        <UsaTextInput v-model="dataItem.access">
          <template #label> Account Access / Account Availability </template>
        </UsaTextInput>

        <div>
          <div class="inline-input-left">
            <UsaTextInput v-model="dataItem.description">
              <template #label> Data Description </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-right">
            <UsaTextInput v-model="dataItem.source">
              <template #label> Source Data Location </template>
            </UsaTextInput>
          </div>
        </div>

        <UsaSelect
          v-model="dataItem.classification"
          :options="classificationOptions"
        >
          <template #label> Data Classification </template>
        </UsaSelect>

        <div class="input-group" style="margin-top: 1em">
          <div v-for="(label, labelIndex) in dataItem.labels" :key="labelIndex">
            <div class="inline-input-left">
              <UsaTextInput v-model="label.description">
                <template #label> Label Description </template>
              </UsaTextInput>
            </div>

            <div class="inline-input-right">
              <UsaTextInput v-model="label.percentage" type="number">
                <template #label> Percentage </template>
              </UsaTextInput>
            </div>
            <div class="inline-button">
              <DeleteButton @click="deleteLabel(dataItemIndex, labelIndex)">
                Delete label
              </DeleteButton>
            </div>
          </div>

          <AddButton class="margin-button" @click="addLabel(dataItemIndex)">
            Add additional label
          </AddButton>
        </div>

        <div class="input-group" style="margin-top: 1em">
          <div
            v-for="(field, schema_index) in dataItem.fields"
            :key="schema_index"
          >
            <h3 class="no-margin-sub-header">
              Data Schema {{ dataItemIndex + 1 }} - {{ schema_index + 1 }}
            </h3>
            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="field.name">
                  <template #label> Field Name </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="field.description">
                  <template #label> Field Description </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="field.type">
                  <template #label> Field Type </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="field.expected_values">
                  <template #label> Expected Values </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="field.missing_values">
                  <template #label> Missing Values </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="field.special_values">
                  <template #label> Special Values </template>
                </UsaTextInput>
              </div>
            </div>
            <DeleteButton
              class="margin-button"
              @click="deleteSchema(dataItemIndex, schema_index)"
            >
              Delete schema
            </DeleteButton>
            <hr />
          </div>

          <AddButton class="margin-button" @click="addSchema(dataItemIndex)">
            Add additional schema
          </AddButton>
        </div>

        <UsaTextInput v-model="dataItem.rights">
          <template #label>
            Data Rights
            <InfoIcon>
              Are there particular ways in which the data can and cannot be
              used?
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="dataItem.policies">
          <template #label>
            Data Policies
            <InfoIcon>
              Are there policies that govern the data and its use, such as
              Personally Identifiable Information [PII]?
            </InfoIcon>
          </template>
        </UsaTextInput>

        <DeleteButton
          class="margin-button"
          @click="deleteDataItem(dataItemIndex)"
        >
          Delete data item
        </DeleteButton>
        <hr />
      </div>
      <AddButton class="margin-button" @click="addDataItem()">
        Add data item
      </AddButton>
    </div>

    <h3>Comments</h3>
    <p>Free-form comments from model developers and system integrators.</p>
    <div v-for="(comment, commentIndex) in form.comments" :key="commentIndex">
      <UsaTextInput v-model="comment.content"> </UsaTextInput>
    </div>

    <!-- TODO: Implement this visualization -->
    <h3>Quantitative Analysis</h3>
    <p>No quantitative analysis included with this report.</p>

    <div style="text-align: right; margin-top: 1em">
      <UsaButton class="secondary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" disabled @click="exportReport()">
        Export
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const userInputArtifactId = ref("");
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);

const findings = ref(null);
const form = ref({
  artifact_type: "report",
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
  validated_spec_id: "",
  comments: [{ content: "" }],
  quantitative_analysis: {},
});

// TODO: Pull these from the schema
const problemTypeOptions = [
  { value: "classification", text: "Classification" },
  { value: "clustering", text: "Clustering" },
  { value: "detection", text: "Detection" },
  { value: "trend", text: "Trend" },
  { value: "alert", text: "Alert" },
  { value: "forecasting", text: "Forecasting" },
  { value: "content_generation", text: "Content Generation" },
  { value: "benchmarking", text: "Benchmarking" },
  { value: "goals", text: "Goals" },
  { value: "other", text: "Other" },
];

// TODO: Pull these from the schema
const classificationOptions = [
  { value: "unclassified", text: "Unclassified" },
  {
    value: "cui",
    text: "Controlled Unclassified Information (CUI)",
  },
  {
    value: "pii",
    text: "Personally Identifiable Information (PII)",
  },
  {
    value: "phi",
    text: "Protected Health Information (PHI)",
  },
  { value: "other", text: "Other" },
];

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
      async onResponse({ response }) {
        if (response.ok) {
          if (isValidReport(response._data)) {
            form.value = response._data.body;
            const problemType = response._data.body.nc_data.system.problem_type;
            if (
              problemTypeOptions.find((x) => x.value === problemType)?.value !==
              undefined
            ) {
              form.value.nc_data.system.problem_type = problemTypeOptions.find(
                (x) => x.value === problemType,
              )?.value;
            }

            // Setting .value for each classification item to work in the select
            response._data.body.nc_data.data.forEach((item) => {
              const classification = item.classification;
              if (
                classificationOptions.find((x) => x.value === classification)
                  ?.value !== undefined
              ) {
                item.classification = classificationOptions.find(
                  (x) => x.value === classification,
                )?.value;
              }
            });

            if (response._data.body.validated_spec_id) {
              form.value.validated_spec_id =
                response._data.body.validated_spec_id;
              const validatedSpec = await fetchArtifact(
                token.value,
                model,
                version,
                form.value.validated_spec_id,
              );
              findings.value = loadFindings(validatedSpec);
            }
          }
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

  const artifact = {
    header: {
      identifier,
      type: "report",
      timestamp: -1,
      creator: "",
    },
    body: form.value,
  };

  if (isValidReport(artifact)) {
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
            if (response.status === 409) {
              conflictErrorAlert();
            } else {
              handleHttpError(
                response.status,
                response._data.error_description,
              );
            }
          },
        },
      );
      successfulArtifactSubmission("report", identifier);
      forceSaveParam.value = true;
    } catch {}
  } else {
    console.log("Invalid report.");
  }
}

// Export the current report.
function exportReport() {
  alert("Report export is not currently implemented.");
}

function addGoal() {
  form.value.nc_data.system.goals.push({
    description: "",
    metrics: [{ description: "", baseline: "" }],
  });
}

function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    form.value.nc_data.system.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex: number) {
  form.value.nc_data.system.goals[goalIndex].metrics.push({
    description: "",
    baseline: "",
  });
}

function deleteMetric(goalIndex: number, metricIndex: number) {
  if (confirm("Are you sure you want to delete this metric?")) {
    form.value.nc_data.system.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}

function addDataItem() {
  form.value.nc_data.data.push({
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
  });
}

function deleteDataItem(dataItemIndex: number) {
  if (confirm("Are you sure you want to delete this data item?")) {
    form.value.nc_data.data.splice(dataItemIndex, 1);
  }
}

function addLabel(dataItemIndex: number) {
  form.value.nc_data.data[dataItemIndex].labels.push({
    name: "",
    description: "",
    percentage: 0,
  });
}

function deleteLabel(dataItemIndex: number, labelIndex: number) {
  if (confirm("Are you sure you want to delete this label?")) {
    form.value.nc_data.data[dataItemIndex].labels.splice(labelIndex, 1);
  }
}

function addSchema(dataItemIndex: number) {
  form.value.nc_data.data[dataItemIndex].fields.push({
    name: "",
    description: "",
    type: "",
    expected_values: "",
    missing_values: "",
    special_values: "",
  });
}

function deleteSchema(dataItemIndex: number, fieldIndex: number) {
  if (confirm("Are you sure you want to delete this field?")) {
    form.value.nc_data.data[dataItemIndex].fields.splice(fieldIndex, 1);
  }
}
</script>
