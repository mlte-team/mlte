<template>
  <NuxtLayout name="base-layout">
    <title>Artifact Store</title>
    <template #page-title>Artifact Store</template>
    <template #right-sidebar>
      <div>
        <UsaTextInput
          v-model="newModelIdentifier"
          @keyup.enter="submitNewModel(newModelIdentifier)"
        >
          <template #label> New Model </template>
        </UsaTextInput>
        <UsaButton
          class="secondary-button margin-button"
          style="margin-left: 0px"
          @click="submitNewModel(newModelIdentifier)"
        >
          Create Model
        </UsaButton>

        <UsaTextInput
          v-model="newVersionIdentifier"
          :disabled="selectedModel === ''"
          @keyup.enter="submitNewVersion(selectedModel, newVersionIdentifier)"
        >
          <template #label> New Version for: {{ selectedModel }} </template>
        </UsaTextInput>
        <UsaButton
          class="secondary-button margin-button"
          style="margin-left: 0px"
          @click="submitNewVersion(selectedModel, newVersionIdentifier)"
        >
          Create Version
        </UsaButton>
      </div>
    </template>

    <!-- <UsaBreadcrumb :items="path" /> -->
    <div style="display: flex">
      <div class="model-version-div">
        <UsaSelect
          :options="modelOptions"
          :model-value="selectedModel"
          @update:model-value="selectModel($event, true)"
        >
          <template #label>Model</template>
        </UsaSelect>
        <br />
      </div>

      <div class="model-version-div">
        <UsaSelect
          :options="versionOptions"
          :model-value="selectedVersion"
          @update:model-value="selectVersion($event)"
        >
          <template #label>Version</template>
        </UsaSelect>
        <br />
      </div>

      <div>
        <!-- Placeholder for when the search functionality is implemented
        <label class="usa-label" style="margin-top: 0px;">Search</label>
        <UsaTextInput v-model="searchInput" style="width: 100%;"/> -->
      </div>
    </div>

    <UsaAccordion multiselectable bordered>
      <UsaAccordionItem label="Negotiation Cards">
        <div class="scrollable-table-div">
          <p>
            A negotiation card is a document with a series of discussion points
            to be documented during a negotiation between all project
            stakeholders at the project's outset. It is then used as a reference
            throughout development and is updated at prescribed negotiation
            points.
          </p>
          <table class="table usa-table usa-table--borderless">
            <thead>
              <tr>
                <th data-sortable scope="col" role="columnheader">ID</th>
                <th data-sortable scope="col" role="columnheader">Timestamp</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="card in negotiationCards" :key="card.id">
                <th scope="row">{{ card.id }}</th>
                <td>{{ card.timestamp }}</td>
                <td>
                  <NuxtLink
                    :to="{
                      path: '/negotiation-card',
                      query: {
                        model: card.model,
                        version: card.version,
                        artifactId: card.id,
                      },
                    }"
                  >
                    <UsaButton class="primary-button"> Edit </UsaButton>
                  </NuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
          <NuxtLink
            :to="{
              path: '/negotiation-card',
              query: {
                model: selectedModel,
                version: selectedVersion,
              },
            }"
          >
            <UsaButton
              :disabled="selectedModel === '' || selectedVersion === ''"
              class="primary-button"
              style="float: left"
            >
              New
            </UsaButton>
          </NuxtLink>
          <p
            v-if="selectedModel === '' || selectedVersion === ''"
            style="float: left; color: red"
          >
            Select a model and version to start a new negotiation card here.
          </p>
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Reports">
        <div class="scrollable-table-div">
          <p>
            A report is a human and machine-readable summary of all knowledge
            gained about a model during the MLTE process.
          </p>
          <table class="table usa-table usa-table--borderless">
            <thead>
              <tr>
                <th data-sortable scope="col" role="columnheader">ID</th>
                <th data-sortable scope="col" role="columnheader">Timestamp</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in reports" :key="report.id">
                <th scope="row">{{ report.id }}</th>
                <td>{{ report.timestamp }}</td>
                <td>
                  <NuxtLink
                    :to="{
                      path: '/report-form',
                      query: {
                        model: report.model,
                        version: report.version,
                        artifactId: report.id,
                      },
                    }"
                  >
                    <UsaButton class="primary-button"> Edit </UsaButton>
                  </NuxtLink>
                  <NuxtLink
                    target="_blank"
                    :to="{
                      path: '/report-export',
                      query: {
                        model: report.model,
                        version: report.version,
                        artifactId: report.id,
                      },
                    }"
                  >
                    <UsaButton class="primary-button"> Export </UsaButton>
                  </NuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
          <NuxtLink
            :to="{
              path: '/report-form',
              query: {
                model: selectedModel,
                version: selectedVersion,
              },
            }"
          >
            <UsaButton
              :disabled="selectedModel === '' || selectedVersion === ''"
              class="primary-button"
              style="float: left"
            >
              New
            </UsaButton>
          </NuxtLink>
          <p
            v-if="selectedModel === '' || selectedVersion === ''"
            style="float: left; color: red"
          >
            Select a model and version to start a new report.
          </p>
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Test Suites">
        <div class="scrollable-table-div">
          <p>
            A test suite defines the model requirements that must be satisfied
            to ensure successful integration with the target system.
          </p>
          <UsaTable
            :headers="testSuiteHeaders"
            :rows="testSuites"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Test Results">
        <div class="scrollable-table-div">
          <p>
            Test Results are produced by combining a specification with its
            corresponding results; this artifact communicates how well a model
            performed against all of its requirements.
          </p>
          <UsaTable
            :headers="testResultHeaders"
            :rows="testResults"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Evidences">
        <div class="scrollable-table-div">
          <p>
            Evidences are the atomic unit of model evaluation in MLTE. A value
            is any artifact produced by a MLTE measurement for the purposes of
            model evaluation.
          </p>
          <UsaTable
            :headers="evidencesHeaders"
            :rows="evidences"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>
    </UsaAccordion>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const newModelIdentifier = ref("");
const newVersionIdentifier = ref("");

const modelOptions = ref<{ value: string; text: string }[]>([]);
const versionOptions = ref<{ value: string; text: string }[]>([]);
const modelList = ref<string[]>([]);

const selectedModel = useCookie("selectedModel", {
  decode(value) {
    return value;
  },
});
selectedModel.value = selectedModel.value || "";
const selectedVersion = useCookie("selectedVersion", {
  decode(value) {
    return value;
  },
});
selectedVersion.value = selectedVersion.value || "";

const testSuiteHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const testResultHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "test_suite_id", label: "Test Suite ID", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const evidencesHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "measurement", label: "Measurement", sortable: true },
  { id: "type", label: "Type", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const negotiationCards = ref<Array<TableItem>>([]);
const testSuites = ref<Array<TableItem>>([]);
const reports = ref<Array<TableItem>>([]);
const testResults = ref<Array<TableItem>>([]);
const evidences = ref<Array<TableItem>>([]);

await populateModelVersionLists();
if (modelOptions.value !== null) {
  const modelList = modelOptions.value.map((model) => {
    return model.value;
  });

  if (!modelList.includes(selectedModel.value)) {
    selectedModel.value = "";
    selectedVersion.value = "";
  }
  if (selectedModel.value !== "") {
    await selectModel(selectedModel.value, false);
    const versionList = versionOptions.value.map((version) => {
      return version.value;
    });
    if (!versionList.includes(selectedVersion.value)) {
      selectedVersion.value = "";
    }
    if (selectedVersion.value !== "") {
      await selectVersion(selectedVersion.value);
    }
  }
}

async function populateModelVersionLists() {
  await $fetch(config.public.apiPath + "/user/me/models/", {
    retry: 0,
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
    onRequestError() {
      requestErrorAlert();
    },
    onResponse({ response }) {
      if (response.ok) {
        modelList.value = response._data;
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });

  modelOptions.value = [];
  if (modelList.value) {
    modelList.value.forEach((modelName: string) => {
      modelOptions.value.push({ value: modelName, text: modelName });
    });
  }
}

// Update the selected model for the artifact store.
async function selectModel(modelName: string, resetSelectedVersion: boolean) {
  selectedModel.value = modelName;
  if (resetSelectedVersion) {
    selectedVersion.value = "";
  }
  if (modelName === "") {
    versionOptions.value = [];
    clearArtifacts();
    return;
  }

  await $fetch(config.public.apiPath + "/model/" + modelName + "/version", {
    retry: 0,
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
    onRequestError() {
      requestErrorAlert();
    },
    onResponse({ response }) {
      if (response.ok && response._data) {
        clearArtifacts();
        selectedModel.value = modelName;
        versionOptions.value = [];
        response._data.forEach((version: string) => {
          versionOptions.value.push({
            value: version,
            text: version,
          });
        });
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });

  versionOptions.value.sort(function (
    a: { value: string; text: string },
    b: { value: string; text: string },
  ) {
    if (a.value < b.value) {
      return -1;
    } else if (a.value > b.value) {
      return 1;
    } else {
      return 0;
    }
  });
}

// Update the selected version for the artifact store.
async function selectVersion(versionName: string) {
  selectedVersion.value = versionName;
  if (selectedVersion.value === "") {
    clearArtifacts();
    return;
  }

  await $fetch(
    config.public.apiPath +
      "/model/" +
      selectedModel.value +
      "/version/" +
      selectedVersion.value +
      "/artifact",
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
        if (response.ok && response._data) {
          populateArtifacts(
            selectedModel.value,
            selectedVersion.value,
            response._data,
          );
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
}

// Populate artifacts for a given model and version.
function populateArtifacts(
  model: string,
  version: string,
  artifactList: Array<Artifact>,
) {
  clearArtifacts();
  artifactList.forEach((artifact: Artifact) => {
    artifact.header.timestamp = new Date(
      artifact.header.timestamp * 1000,
    ).toLocaleString("en-US") as unknown as number;
    // Negotiation card
    if (artifact.header.type === "negotiation_card") {
      if (isValidNegotiation(artifact)) {
        negotiationCards.value.push({
          id: artifact.header.identifier,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
    // Report
    else if (artifact.header.type === "report") {
      if (isValidReport(artifact)) {
        reports.value.push({
          id: artifact.header.identifier,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
    // Test Suite
    else if (artifact.header.type === "test_suite") {
      if (isValidTestSuite(artifact)) {
        testSuites.value.push({
          id: artifact.header.identifier,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
    // Test Results
    else if (artifact.body.artifact_type === "test_results") {
      if (isValidTestResults(artifact)) {
        testResults.value.push({
          id: artifact.header.identifier,
          test_suite_id: artifact.body.test_suite_id,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
    // Evidence
    if (artifact.body.artifact_type === "evidence") {
      if (isValidEvidence(artifact)) {
        evidences.value.push({
          id: artifact.header.identifier.slice(0, -6),
          measurement: artifact.body.metadata.measurement.measurement_class,
          type: artifact.body.value.evidence_type,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
  });
}

// Clear all artifacts from local state.
function clearArtifacts() {
  negotiationCards.value = [];
  reports.value = [];
  testSuites.value = [];
  testResults.value = [];
  evidences.value = [];
}

async function submitNewModel(modelName: string) {
  try {
    await $fetch(config.public.apiPath + "/model/", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: {
        identifier: modelName,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          populateModelVersionLists();
          alert(`Model, ${modelName} has been created.`);
          newModelIdentifier.value = "";
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    });
  } catch (exception) {
    console.log(exception);
  }
}

async function submitNewVersion(modelName: string, versionName: string) {
  try {
    await $fetch(config.public.apiPath + "/model/" + modelName + "/version", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: {
        identifier: versionName,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          selectModel(modelName, false);
          alert(
            `Version, ${versionName} for model, ${modelName} has been created`,
          );
          newVersionIdentifier.value = "";
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    });
  } catch (exception) {
    console.log(exception);
  }
}
</script>

<style>
.scrollable-table-div {
  overflow-y: auto;
  height: 18em;
}

.table {
  width: 100%;
}

.model-version-div {
  width: 34ch;
  margin-right: 1em;
}

.scrollable-div {
  border: 1px solid gray;
  overflow-y: auto;
  height: 11em;
  padding-left: 0.4em;
}
</style>
