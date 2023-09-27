<template>
  <NuxtLayout name="base-layout">
    
    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">MLTE REPORT</h1>

    <h3>Model Summary</h3>
    <UsaTextarea>
      <template #label>
        Summary of the model being evaluated.
      </template>
    </UsaTextarea>

    <h3>Goals of the System</h3>
      <p>Goals or objectives that the model helps to satisfy.</p>
      <div
        v-for="(goal, goalIndex) in form.system.goals"
        :key="goal.description"
      >
        <h3>Goal {{ goalIndex + 1 }}</h3>

        <UsaTextInput v-model="goal.description">
          <template #label> Goal Description </template>
        </UsaTextInput>

      </div>
      <AddButton class="margin-button" @click="addGoal()"> Add goal </AddButton>
      <!--<DeleteButton @click="deleteGoal(goalIndex)">
          Delete goal
        </DeleteButton> -->
    <h3>MLTE Evaluation</h3>
      <p>THIS IS A PLACEHOLDER
        <br />
        <br />
        <br />
        TO DELINEATE A SPACE
        <br />
        <br />
        <br />
        WHERE MLTE EVALUATION RESULTS
        <br />
        <br />
        <br />
        WILL EVENTUALLY LIVE.
        <br />
        <br />
        <br />
      </p>
    
    <h3>Intended Use</h3>
    <UsaTextarea>
      <template #label>
        Description of how the model is intended to be used.
      </template>
    </UsaTextarea>

    <h3>Risks</h3>
    <UsaTextarea>
      <template #label>
        Description of model and system risks.
      </template>
    </UsaTextarea>

    <h3>Data</h3>
    <UsaTextarea>
      <template #label>
        Description of data used to train the model.
      </template>
    </UsaTextarea>

    <h3>Caveats and Recommendations</h3>
    <UsaTextarea>
      <template #label>
        Description of any caveats and recommendations for the system or model.
      </template>
    </UsaTextarea>

    <h3>Quantitative Analysis</h3>
      <p>THIS IS A PLACEHOLDER
        <br />
        <br />
        <br />
        TO REPRESENT THE SPACE
        <br />
        <br />
        <br />
        WHERE FUN AND INFORMATIVE GRAPHS
        <br />
        <br />
        <br />
        WILL EVENTUALLY LIVE!
        <br />
        <br />
        <br />
      </p>

        <div style="text-align: center; margin-top: 1em">
      <UsaButton class="primary-button" @click="submit()"> EXPORT </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/report-card",
    text: "Report",
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
              addGoal();
              const lastGoalIndex = form.value.system.goals.length - 1;

              form.value.system.goals[lastGoalIndex].description = goal.goal;
              form.value.system.goals[lastGoalIndex].metrics[0].description =
                goal.metric;
              form.value.system.goals[lastGoalIndex].metrics[0].baseline =
                goal.baseline;
            },
          );
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
              addLabel(lastDataIndex);
              form.value.data[lastDataIndex].labels[i].description =
                label.label;
              form.value.data[lastDataIndex].labels[i].percentage =
                label.percentage;
            },
          );

          form.value.data[lastDataIndex].rights = document.data_rights;
          form.value.data[lastDataIndex].policies = document.data_policies;

          form.value.data[lastDataIndex].schema.splice(0, 1);
          document.schema.forEach(
            (
              schema: {
                field_name: string;
                field_description: string;
                field_type: string;
                expected_values: string;
                interpret_missing: string;
                interpret_special: string;
              },
              i: number,
            ) => {
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
            },
          );
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
    metrics: [{ description: "", baseline: "" }],
  });
}

function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    form.value.system.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex: number) {
  form.value.system.goals[goalIndex].metrics.push({
    description: "",
    baseline: "",
  });
}

function deleteMetric(goalIndex: number, metricIndex: number) {
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
  form.value.data[dataItemIndex].schema.push({
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
    form.value.data[dataItemIndex].schema.splice(fieldIndex, 1);
  }
}
</script> 