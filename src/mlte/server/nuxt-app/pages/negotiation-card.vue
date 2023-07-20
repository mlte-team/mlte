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
            @change="descriptorUpload('System Context')"
          />

          <label class="usa-label"> Raw Data </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload('Raw Data')"
          />

          <label class="usa-label"> Development Environment </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload('Development Environment')"
          />

          <label class="usa-label"> Production Environment </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload('Production Environment')"
          />
        </div>
      </div>
    </template>

    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">How to use Negotiation Card</h1>
    <p>
      Teams should work through as many of the following items as they can at
      the IMT negotiation point, using the answers to inform initial model
      development. At the SDMT negotiation point, answers should be
      modified/updated according to the results of IMT. As the
      <a href="/TODO">Specification</a> is created, teams should refer to this
      negotiation card to ensure they capture all relevant critical aspects of
      the model and system.
    </p>

    <h2 class="section-header">System Requirements</h2>
    <div class="input-group">
      <h3>Goals</h3>
      <p>Goals or objectives that the model is going to help satisfy.</p>
      <div v-for="(goal, goalIndex) in form.system.goals" :key="goal">
        <h3>Goal {{ goalIndex + 1 }}</h3>

        <UsaTextInput v-model="goal.description">
          <template #label> Goal Description </template>
        </UsaTextInput>

        <h3 class="no-margin-section-header">Metrics</h3>
        <div v-for="(metric, metricIndex) in goal.metrics" :key="metric">
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

    <UsaSelect v-model="form.system.problem_type" :options="problemTypeOptions">
      <template #label>
        ML Problem Type
        <InfoIcon>
          Type of ML problem that the model is intended to solve.
        </InfoIcon>
      </template>
    </UsaSelect>

    <UsaTextInput v-model="form.system.task">
      <template #label>
        ML Task
        <InfoIcon>
          Well-defined task that model is expected to perform, or problem that
          the model is expected to solve.
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.usage_context">
      <template #label>
        Usage Context
        <InfoIcon>
          Who is intended to utilize the system/model; how the results of the
          model are <br />
          going to be used by end users or in the context of a larger system.
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.fp_risk">
      <template #label> False Positive Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.fn_risk">
      <template #label> False Negative Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.other_risks">
      <template #label> Other risks of producing incorrect results </template>
    </UsaTextInput>

    <h2 class="section-header">Data</h2>
    <p>
      Details of the data that will influence development efforts; fill out all
      that are known. For access / availability, record what needs to happen to
      access the data, such as accounts that need to be created or methods for
      data transportation.
    </p>
    <div class="input-group">
      <div v-for="(data_item, dataItemIndex) in form.data" :key="data_item">
        <h3>Data Item {{ dataItemIndex + 1 }}</h3>
        <UsaTextInput v-model="data_item.access">
          <template #label> Account Access / Account Availability </template>
        </UsaTextInput>

        <div>
          <div class="inline-input-left">
            <UsaTextInput v-model="data_item.description">
              <template #label> Data Description </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-right">
            <UsaTextInput v-model="data_item.source">
              <template #label> Source Data Location </template>
            </UsaTextInput>
          </div>
        </div>

        <UsaSelect
          v-model="data_item.classification"
          :options="classificationOptions"
        >
          <template #label> Data Classification </template>
        </UsaSelect>

        <div class="input-group" style="margin-top: 1em">
          <div v-for="(label, labelIndex) in data_item.labels" :key="label">
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
          <div v-for="(schema, schema_index) in data_item.schema" :key="schema">
            <h3 class="no-margin-section-header">
              Data Schema {{ dataItemIndex + 1 }} - {{ schema_index + 1 }}
            </h3>
            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="schema.name">
                  <template #label> Field Name </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="schema.description">
                  <template #label> Field Description </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="schema.type">
                  <template #label> Field Type </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="schema.expected_values">
                  <template #label> Expected Values </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="schema.missing_values">
                  <template #label> Missing Values </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="schema.special_values">
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

        <UsaTextInput v-model="data_item.rights">
          <template #label>
            Data Rights
            <InfoIcon>
              Are there particular ways in which the data can and cannot be
              used?
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="data_item.policies">
          <template #label>
            Data Policies
            <InfoIcon>
              Are there policies that govern the data and its use, such as
              Personally Identifiable Information [PII]?
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="data_item.identifiable_information">
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

    <h2 class="section-header">Model</h2>
    <div class="input-group">
      <h3>Development Compute Resources</h3>
      <p>
        Describe the amount and type of compute resources needed for training.
      </p>
      <div>
        <div class="inline-input-left">
          <UsaTextInput
            v-model="form.model.development.resources.gpus"
            type="number"
          >
            <template #label> Graphics Processing Units (GPUs) </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput
            v-model="form.model.development.resources.cpus"
            type="number"
          >
            <template #label> Central Processing Units (CPUs) </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput
            v-model="form.model.development.resources.memory"
            type="number"
          >
            <template #label> Memory </template>
            <template #input-suffix> GB </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput
            v-model="form.model.development.resources.storage"
            type="number"
          >
            <template #label> Storage </template>
            <template #input-suffix> GB </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <UsaTextarea v-model="form.model.production.environment.integration">
      <template #label>
        Integration
        <InfoIcon>
          Describe how the model will be integrated into the system; this likely
          <br />
          includes descriptions of model deployment, application hosting, etc.
        </InfoIcon>
      </template>
    </UsaTextarea>

    <UsaTextarea v-model="form.model.production.environment.output">
      <template #label>
        Output
        <InfoIcon>
          Describe the output format and specification needed for the system to
          ingest model results.
        </InfoIcon>
      </template>
    </UsaTextarea>

    <div class="input-group" style="margin-top: 1em">
      <h3>Production Compute Resources</h3>
      <p>
        Describe the hardware and software requirements including amount of
        compute resources needed for inference.
      </p>
      <div>
        <div class="inline-input-left">
          <UsaTextInput
            v-model="form.model.production.resources.gpus"
            type="number"
          >
            <template #label> Graphics Processing Units (GPUs) </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput
            v-model="form.model.production.resources.cpus"
            type="number"
          >
            <template #label> Central Processing Units (CPUs) </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput
            v-model="form.model.production.resources.memory"
            type="number"
          >
            <template #label> Memory </template>
            <template #input-suffix> GB </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput
            v-model="form.model.production.resources.storage"
            type="number"
          >
            <template #label> Storage </template>
            <template #input-suffix> GB </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <div style="text-align: right; margin-top: 1em">
      <UsaButton class="secondary-button" @click="cancel()"> Cancel </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup>
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/negotiation-store",
    text: "Negotiation Card",
  },
]);

const form = ref({
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
    problem_type: "",
    task: "",
    usage_context: "",
    fp_risk: "",
    fn_risk: "",
    other_risks: "",
  },
  data: [
    {
      access: "",
      description: "",
      source: "",
      classification: "",
      labels: [
        {
          description: "",
          percentage: 0,
        },
      ],
      schema: [
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
  model: {
    development: {
      resources: {
        gpus: 0,
        cpus: 0,
        memory: 0,
        storage: 0,
      },
    },
    production: {
      environment: {
        integration: "",
        output: "",
      },
      resources: {
        gpus: 0,
        cpus: 0,
        memory: 0,
        storage: 0,
      },
    },
  },
});

const problemTypeOptions = [
  { value: "Classification", text: "Classification" },
  { value: "Clustering", text: "Clustering" },
  { value: "Content Generation", text: "Content Generation" },
  { value: "Detection", text: "Detection" },
  { value: "Trend", text: "Trend" },
  { value: "Alert", text: "Alert" },
  { value: "Forecasting", text: "Forecasting" },
  { value: "Summarization", text: "Summarization" },
  { value: "Benchmarking", text: "Benchmarking" },
  { value: "Goals", text: "Goals" },
  { value: "Other", text: "Other" },
];

const classificationOptions = [
  { value: "Unclassified", text: "Unclassified" },
  {
    value: "Controlled Unclassified Information (CUI)",
    text: "Controlled Unclassified Information (CUI)",
  },
  {
    value: "Personally Identifiable Information (PII)",
    text: "Personally Identifiable Information (PII)",
  },
  {
    value: "Protected Health Information (PHI)",
    text: "Protected Health Information (PHI)",
  },
  { value: "Other", text: "Other" },
];

function cancel() {
  if (
    confirm(
      "Are you sure you want to leave this page? All changes will be lost.",
    )
  ) {
    location.href = "/";
  }
}

function submit() {
  console.log(form.value);
  console.log(useRoute().query.namespace);
}

function descriptorUpload(descriptorName) {
  if (event.target.files[0]) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (res) => {
      try {
        const document = JSON.parse(res.target.result);
        if (descriptorName === "System Context") {
          document.goals.forEach((goal, i) => {
            addGoal();
            const lastGoalIndex = form.value.system.goals.length - 1;

            form.value.system.goals[lastGoalIndex].description = goal.goal;
            form.value.system.goals[lastGoalIndex].metrics[0].description =
              goal.metric;
            form.value.system.goals[lastGoalIndex].metrics[0].baseline =
              goal.baseline;
          });
          form.value.system.task = document.task;
          form.value.system.problem_type = document.ml_problem_type.ml_problem;
          form.value.system.usage_context = document.usage_context;
          form.value.system.fp_risk = document.risks.risk_fp;
          form.value.system.fn_risk = document.risks.risk_fn;
          form.value.system.other_risks = document.risks.risk_other;
        } else if (descriptorName === "Raw Data") {
          addDataItem();
          const lastDataIndex = form.value.data.length - 1;

          let dataSourcesStr = "";
          document.data_sources.forEach((source, i) => {
            if (source.data_source === "Other") {
              dataSourcesStr += source.other_source;
            } else {
              dataSourcesStr += source.data_source;
            }

            if (i + 1 < document.data_sources.length) {
              dataSourcesStr += ", ";
            }
          });
          form.value.data[lastDataIndex].source = dataSourcesStr;

          form.value.data[lastDataIndex].labels.splice(0, 1);
          document.labels_distribution.forEach((label, i) => {
            addLabel(lastDataIndex);
            form.value.data[lastDataIndex].labels[i].description = label.label;
            form.value.data[lastDataIndex].labels[i].percentage =
              label.percentage;
          });

          form.value.data[lastDataIndex].rights = document.data_rights;
          form.value.data[lastDataIndex].policies = document.data_policies;

          form.value.data[lastDataIndex].schema.splice(0, 1);
          document.schema.forEach((schema, i) => {
            addSchema(lastDataIndex);
            form.value.data[lastDataIndex].schema[i].name = schema.field_name;
            form.value.data[lastDataIndex].schema[i].description =
              schema.field_description;
            form.value.data[lastDataIndex].schema[i].type = schema.field_type;
            form.value.data[lastDataIndex].schema[i].expected_values =
              schema.expected_values;
            form.value.data[lastDataIndex].schema[i].missing_values =
              schema.interpret_missing;
            form.value.data[lastDataIndex].schema[i].special_values =
              schema.interpret_special;
          });
        } else if (descriptorName === "Development Environment") {
          form.value.model.development.resources.gpus =
            document.computing_resources.gpu;
          form.value.model.development.resources.cpus =
            document.computing_resources.cpu;
          form.value.model.development.resources.memory =
            document.computing_resources.memory;
          form.value.model.development.resources.storage =
            document.computing_resources.storage;

          let outputString = "";
          if (form.value.model.production.environment.output !== "") {
            outputString += "\n\n";
          }
          document.downstream_components.forEach((component, i) => {
            outputString +=
              "Component Name: " + component.component_name + "\n";
            outputString += "ML Component: " + component.ml_component + "\n";
            component.input_spec.forEach((spec, j) => {
              outputString += spec.item_name + "\n";
              outputString += spec.item_description + "\n";
              outputString += spec.item_type + "\n";
              outputString += spec.expected_values + "\n";
            });
            outputString += "\n";
          });
          outputString = outputString.substring(0, outputString.length - 2);
          form.value.model.production.environment.output += outputString;
        } else if (descriptorName === "Production Environment") {
          form.value.model.production.resources.gpus =
            document.computing_resources.gpu;
          form.value.model.production.resources.cpus =
            document.computing_resources.cpu;
          form.value.model.production.resources.memory =
            document.computing_resources.memory;
          form.value.model.production.resources.storage =
            document.computing_resources.storage;
        }
      } catch (err) {
        console.error("Invalid JSON or error in parsing file.");
      }
    };
    reader.readAsText(file);
  }
}

function addGoal() {
  form.value.system.goals.push({
    description: "",
    metrics: [{ performance_metrics: "", baseline: "" }],
  });
}

function deleteGoal(goalIndex) {
  if (confirm("Are you sure you want to delete this goal?")) {
    form.value.system.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex) {
  form.value.system.goals[goalIndex].metrics.push({
    description: "",
    baseline: "",
  });
}

function deleteMetric(goalIndex, metricIndex) {
  if (confirm("Are you sure you want to delete this metric?")) {
    form.value.system.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}

function addDataItem() {
  form.value.data.push({
    access: "",
    description: "",
    source: "",
    classification: "",
    labels: [
      {
        description: "",
        percentage: 0,
      },
    ],
    schema: [
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

function deleteDataItem(dataItemIndex) {
  if (confirm("Are you sure you want to delete this data item?")) {
    form.value.data.splice(dataItemIndex, 1);
  }
}

function addLabel(dataItemIndex) {
  form.value.data[dataItemIndex].labels.push({
    description: "",
    percentage: 0,
  });
}

function deleteLabel(dataItemIndex, labelIndex) {
  if (confirm("Are you sure you want to delete this label?")) {
    form.value.data[dataItemIndex].labels.splice(labelIndex, 1);
  }
}

function addSchema(dataItemIndex) {
  form.value.data[dataItemIndex].schema.push({
    name: "",
    description: "",
    type: "",
    expected_values: "",
    missing_values: "",
    special_values: "",
  });
}

function deleteSchema(dataItemIndex, fieldIndex) {
  if (confirm("Are you sure you want to delete this field?")) {
    form.value.data[dataItemIndex].schema.splice(fieldIndex, 1);
  }
}
</script>
