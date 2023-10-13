<template>
  <NuxtLayout name="base-layout">
    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">MLTE REPORT</h1>

    <h2>Model Summary</h2>
    <p>A summary of the model under evaluation.</p>

    <UsaTextInput :model-value="form.summary.problem_type">
      <template #label> Problem Type </template>
    </UsaTextInput>
    <UsaTextInput :model-value="form.summary.task">
      <template #label> Task </template>
    </UsaTextInput>

    <!-- Kept the goals section consistent with the negotiation card.
    Probably need to rewrite once we figure out how we want to pull 
    sections from the negotiation card.-->

    <h2>Performance</h2>
    <p>Model performance evaluation.</p>

    <div
      v-for="(goal, goalIndex) in form.performance.goals"
      :key="goal.description"
    >
      <h3>Goal {{ goalIndex + 1 }}</h3>

      <UsaTextInput v-model="goal.description">
        <template #label> Goal Description </template>
      </UsaTextInput>
      <h4 class="no-margin-section-header">Metrics</h4>
      <div v-for="(metric, metricIndex) in goal.metrics" :key="metricIndex">
        <div class="inline-input-left">
          <UsaTextInput v-model="metric.description">
            <template #label> Description </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="metric.baseline">
            <template #label> Baseline </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <h3>MLTE Evaluation</h3>
    <p>TODO</p>

    <h2>Intended Use</h2>
    <p>A description of how the model is intended to be used.</p>
    <UsaTextarea :model-value="form.intended_use.context"></UsaTextarea>

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
      <h3>Production Resource Requirements</h3>
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

    <h3>Risks</h3>
    <UsaTextInput v-model="form.risks.fp">
      <template #label> False Positive Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.risks.fn">
      <template #label> False Negative Risk </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.risks.other">
      <template #label> Other risks of producing incorrect results </template>
    </UsaTextInput>

    <h3>Data</h3>
    <p>A description of the data used to train the model.</p>

    <div class="input-group">
      <div v-for="(dataItem, dataItemIndex) in form.data" :key="dataItemIndex">
        <h4>Dataset {{ dataItemIndex + 1 }}</h4>
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

        <UsaTextInput v-model="dataItem.classification">
          <template #label> Data Classification </template>
        </UsaTextInput>

        <div class="input-group" style="margin-top: 1em">
          <h4 class="no-margin-section-header">Data Ontology</h4>
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
          </div>
        </div>

        <div class="input-group" style="margin-top: 1em">
          <h4 class="no-margin-section-header">Data Schema</h4>
          <div v-for="(field, fieldIndex) in dataItem.fields" :key="fieldIndex">
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
            <hr />
          </div>
        </div>

        <UsaTextInput v-model="dataItem.rights">
          <template #label> Data Rights </template>
        </UsaTextInput>

        <UsaTextInput v-model="dataItem.policies">
          <template #label> Data Policies </template>
        </UsaTextInput>

        <UsaTextInput v-model="dataItem.identifiable_information">
          <template #label> Identifiable Information </template>
        </UsaTextInput>
      </div>
    </div>

    <h3>Comments</h3>
    <p>Free-form comments from model developers and system integrators.</p>

    <div v-for="(comment, commentIndex) in form.comments" :key="commentIndex">
      <UsaTextInput v-model="comment.content">
      </UsaTextInput>
    </div>

    <h3>Quantitative Analysis</h3>
    <p>No quantitative analysis included with this report.</p>

    <!--Added in the submit and cancel buttons and functions from the negotiation card.
    It doesn't seem to me that the submit button is working, but I don't know 
    how to test it appropriately. -->
    <div style="text-align: center; margin-top: 1em">
      <UsaButton class="primary-button" @click="exportReport()"> Export </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import {
  requestErrorAlert,
  responseErrorAlert,
} from "../composables/error-handling";

import { isValidReport } from "../composables/artifact-validation.ts";

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

// Rewrote the form so that every item is at the top level;
// not sure that is exactly what we want but I figured it is a starting point.
const form = ref({
  summary: {
    problem_type: "",
    task: "",
  },
  performance: {
    goals: [],
    mlte_evaluation: "",
  },
  intended_use: {
    context: "",
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
  data: [],
  comments: [],
  analysis: {},
});

if (useRoute().query.artifactId !== undefined) {
  const namespace = useRoute().query.namespace;
  const model = useRoute().query.model;
  const version = useRoute().query.version;
  const artifactId = useRoute().query.artifactId;

  await useFetch(
    "http://localhost:8080/api/namespace/" +
      namespace +
      "/model/" +
      model +
      "/version/" +
      version +
      "/artifact/" +
      artifactId,
    {
      retry: 0,
      method: "GET",
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        form.value.summary.problem_type = capitalizeWord(
          response._data.body.summary.problem_type,
        );
        form.value.summary.task = capitalizeString(
          response._data.body.summary.task,
        );

        form.value.performance.goals = response._data.body.performance.goals;

        form.value.intended_use.context =
          response._data.body.intended_use.usage_context;
        form.value.intended_use.production_requirements.integration =
          response._data.body.intended_use.production_requirements.integration;
        form.value.intended_use.production_requirements.interface =
          response._data.body.intended_use.production_requirements.interface;
        form.value.intended_use.production_requirements.resources =
          response._data.body.intended_use.production_requirements.resources;

        form.value.risks = response._data.body.risks;

        form.value.data = response._data.body.data;

        form.value.comments = response._data.body.comments;
      },
      onResponseError() {
        responseErrorAlert();
      },
    },
  );
}

// Capitalize all words in a string.
function capitalizeString(string: string) {
  return string
    .split(" ")
    .map((word) => capitalizeWord(word))
    .join(" ");
}

// Capitalize a word.
function capitalizeWord(word: string) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

// Export the current report.
function exportReport() {
  alert(
    "Report export is not currently implemented.",
  );
}

</script>
