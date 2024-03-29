<template>
  <NuxtLayout name="base-layout">
    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">MLTE REPORT</h1>

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
      v-model="form.summary.problem_type"
      :options="problemTypeOptions"
    >
      <template #label>
        Problem Type
        <InfoIcon> Type of ML problem the model is intended to solve </InfoIcon>
      </template>
    </UsaSelect>

    <UsaTextInput :model-value="form.summary.task">
      <template #label> Task </template>
    </UsaTextInput>

    <h2 class="section-header">Performance</h2>
    <p>Model performance evaluation.</p>
    <div class="input-group">
      <h3>Goals</h3>
      <p>Goals or objectives that the model is going to help satisfy.</p>
      <div v-for="(goal, goalIndex) in form.performance.goals" :key="goalIndex">
        <h3>Goal {{ goalIndex + 1 }}</h3>

        <UsaTextInput v-model="goal.description">
          <template #label> Goal Description </template>
        </UsaTextInput>

        <h3 class="no-margin-section-header">Metrics</h3>
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
    <p>A description of how the model is intended to be used.</p>
    <UsaTextarea :model-value="form.intended_use.usage_context"></UsaTextarea>

    <UsaTextarea
      v-model="form.intended_use.production_requirements.integration"
    >
      <template #label>
        A description of model integration practices.
      </template>
    </UsaTextarea>

    <UsaTextInput
      v-model="
        form.intended_use.production_requirements.interface.input.description
      "
    >
      <template #label> Model input description. </template>
    </UsaTextInput>

    <UsaTextInput
      v-model="
        form.intended_use.production_requirements.interface.output.description
      "
    >
      <template #label> Mode output description. </template>
    </UsaTextInput>

    <div class="input-group" style="margin-top: 1em">
      <h3>Production Compute Resources</h3>
      <p>
        Describe the hardware and software requirements including amount of
        compute resources needed for inference.
      </p>
      <div>
        <div class="inline-input-left">
          <UsaTextInput
            v-model="form.intended_use.production_requirements.resources.gpu"
          >
            <template #label> GPU </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput
            v-model="form.intended_use.production_requirements.resources.cpu"
          >
            <template #label> CPU </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput
            v-model="form.intended_use.production_requirements.resources.memory"
          >
            <template #label> Memory </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput
            v-model="
              form.intended_use.production_requirements.resources.storage
            "
          >
            <template #label> Storage </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <h2 class="section-header">Risks</h2>
    <UsaTextInput v-model="form.risks.fp">
      <template #label> False Positive Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.risks.fn">
      <template #label> False Negative Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.risks.other">
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
      <div v-for="(dataItem, dataItemIndex) in form.data" :key="dataItemIndex">
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
            <h3 class="no-margin-section-header">
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

        <UsaTextInput v-model="dataItem.identifiable_information">
          <template #label> Identifiable Information </template>
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
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/here",
    text: "Report",
  },
]);

const userInputArtifactId = ref("");
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);

const findings = ref(null);
const form = ref({
  artifact_type: "report",
  summary: {
    problem_type: "classification",
    task: "",
  },
  performance: {
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
    validated_spec_id: null,
  },
  intended_use: {
    usage_context: "",
    production_requirements: {
      integration: "",
      interface: {
        input: {
          description: "",
        },
        output: {
          description: "",
        },
      },
      resources: {
        cpu: "",
        gpu: "",
        memory: "",
        storage: "",
      },
    },
  },
  risks: {
    fp: "",
    fn: "",
    other: "",
  },
  data: [
    {
      access: "",
      description: "",
      source: "",
      classification: "unclassified",
      labels: [
        {
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
      identifiable_information: "",
    },
  ],
  comments: [
    {
      content: "",
    },
  ],
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
        if (isValidReport(response._data)) {
          form.value = response._data.body;
          const problemType = response._data.body.summary.problem_type;
          if (
            problemTypeOptions.find((x) => x.value === problemType)?.value !==
            undefined
          ) {
            form.value.summary.problem_type = problemTypeOptions.find(
              (x) => x.value === problemType,
            )?.value;
          }

          // Setting .value for each classification item to work in the select
          response._data.body.data.forEach((item) => {
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

          if (response._data.body.performance.validated_spec_id) {
            form.value.performance.validated_spec_id =
              response._data.body.performance.validated_spec_id;
            const validatedSpec = await fetchArtifact(
              token.value,
              model,
              version,
              form.value.performance.validated_spec_id,
            );
            findings.value = loadFindings(validatedSpec);
          }
        }
      },
      onResponseError() {
        responseErrorAlert();
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
              responseErrorAlert();
            }
          },
        },
      );
      successfulSubmission("report", identifier);
      forceSaveParam.value = true;
    } catch (error) {
      console.log("Error in fetch.");
      console.log(error);
    }
  } else {
    console.log("Invalid report.");
  }
}

// Load findings from a validated specication.
function loadFindings(proxyObject: any) {
  const findings = [];
  // TODO(Kyle): Standardize conversion of proxy objects.
  const validatedSpec = JSON.parse(JSON.stringify(proxyObject));
  validatedSpec.body.spec.properties.forEach((property) => {
    // TODO(Kyle): This is not portable to some browsers.
    const results = new Map(
      Object.entries(validatedSpec.body.results[property.name]),
    );
    results.forEach((value) => {
      const finding = {
        status: value.type,
        property: property.name,
        measurement: value.metadata.measurement_type,
        evidence_id: value.metadata.identifier.name,
        message: value.message,
      };
      findings.push(finding);
    });
  });
  return findings;
}

// Export the current report.
function exportReport() {
  alert("Report export is not currently implemented.");
}

function addGoal() {
  form.value.performance.goals.push({
    description: "",
    metrics: [{ description: "", baseline: "" }],
  });
}

function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    form.value.performance.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex: number) {
  form.value.performance.goals[goalIndex].metrics.push({
    description: "",
    baseline: "",
  });
}

function deleteMetric(goalIndex: number, metricIndex: number) {
  if (confirm("Are you sure you want to delete this metric?")) {
    form.value.performance.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}

function addDataItem() {
  form.value.data.push({
    access: "",
    description: "",
    source: "",
    classification: "unclassified",
    labels: [
      {
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
    identifiable_information: "",
  });
}

function deleteDataItem(dataItemIndex: number) {
  if (confirm("Are you sure you want to delete this data item?")) {
    form.value.data.splice(dataItemIndex, 1);
  }
}

function addLabel(dataItemIndex: number) {
  form.value.data[dataItemIndex].labels.push({
    description: "",
    percentage: 0,
  });
}

function deleteLabel(dataItemIndex: number, labelIndex: number) {
  if (confirm("Are you sure you want to delete this label?")) {
    form.value.data[dataItemIndex].labels.splice(labelIndex, 1);
  }
}

function addSchema(dataItemIndex: number) {
  form.value.data[dataItemIndex].fields.push({
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
    form.value.data[dataItemIndex].fields.splice(fieldIndex, 1);
  }
}
</script>
