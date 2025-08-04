<template>
  <NuxtLayout name="base-layout">
    <title>Artifact Store</title>
    <template #page-title>Artifact Store</template>
    <template #right-sidebar>
      <div>
        <UsaTextInput
          v-model="newModelIdentifier"
          @keyup.enter="createNewModel(newModelIdentifier)"
        >
          <template #label> New Model </template>
        </UsaTextInput>
        <UsaButton
          class="secondary-button margin-button"
          style="margin-left: 0px"
          @click="createNewModel(newModelIdentifier)"
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
                      path: '/report-view',
                      query: {
                        model: report.model,
                        version: report.version,
                        artifactId: report.id,
                      },
                    }"
                  >
                    <UsaButton class="primary-button"> View </UsaButton>
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
const newModelIdentifier = ref("");
const newVersionIdentifier = ref("");

const modelOptions = ref<Array<SelectOption>>([]);
const versionOptions = ref<Array<SelectOption>>([]);
const modelList = ref<Array<string>>([]);

const selectedModel = useCookie("selectedModel", {
  decode(value) {
    return decodeURIComponent(value);
  },
});

selectedModel.value = selectedModel.value || "";
const selectedVersion = useCookie("selectedVersion", {
  decode(value) {
    return decodeURIComponent(value);
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

await populateModelList();
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

// Populate the list of Model options.
async function populateModelList() {
  const models: Array<string> = await getUserModels();
  if (models) {
    modelList.value = models;
    modelOptions.value = [];
    modelList.value.forEach((modelName: string) => {
      modelOptions.value.push(new SelectOption(modelName, modelName));
    });
  }
}

/**
 * Update the selected Model for the artifact store.
 *
 * @param {string} modelName Model to select
 * @param {boolean} resetSelectedVersion Flag to reset selectedVersion or not
 */
async function selectModel(modelName: string, resetSelectedVersion: boolean) {
  selectedModel.value = modelName;
  if (resetSelectedVersion) {
    selectedVersion.value = "";
    clearArtifacts();
  }
  if (modelName === "") {
    versionOptions.value = [];
    clearArtifacts();
    return;
  }

  const modelVersions = await getModelVersions(modelName);
  if (modelVersions) {
    versionOptions.value = [];
    modelVersions.forEach((version: string) => {
      versionOptions.value.push(new SelectOption(version, version));
    });
  }
}

/**
 * Update the selected version and load its artifacts.
 *
 * @param {string} versionName Version to select
 */
async function selectVersion(versionName: string) {
  selectedVersion.value = versionName;
  if (selectedVersion.value === "") {
    clearArtifacts();
    return;
  }

  const versionArtifacts: Array<ArtifactModel> = await getVersionArtifacts(
    selectedModel.value,
    selectedVersion.value,
  );
  if (versionArtifacts) {
    populateArtifacts(
      selectedModel.value,
      selectedVersion.value,
      versionArtifacts,
    );
  }
}

/**
 * Populate Artifacts for a given Model and Version.
 *
 * @param {string} model Model that contains the Version
 * @param {string} version Version that contains the Artifacts
 * @param {Array<ArtifactModel>} artifactList List of Artifacts of the Model Version
 */
function populateArtifacts(
  model: string,
  version: string,
  artifactList: Array<ArtifactModel>,
) {
  clearArtifacts();
  artifactList.forEach((artifact: ArtifactModel) => {
    artifact.header.timestamp = new Date(
      artifact.header.timestamp * 1000,
    ).toLocaleString("en-US") as unknown as number;
    // Negotiation card
    if (artifact.body.artifact_type === "negotiation_card") {
      if (isValidNegotiation(artifact)) {
        negotiationCards.value.push(
          new TableItem(
            artifact.header.identifier,
            artifact.header.timestamp,
            model,
            version,
          ),
        );
      }
    }
    // Report
    else if (artifact.body.artifact_type === "report") {
      if (isValidReport(artifact)) {
        reports.value.push(
          new TableItem(
            artifact.header.identifier,
            artifact.header.timestamp,
            model,
            version,
          ),
        );
      }
    }
    // Test Suite
    else if (artifact.body.artifact_type === "test_suite") {
      if (isValidTestSuite(artifact)) {
        testSuites.value.push(
          new TableItem(
            artifact.header.identifier,
            artifact.header.timestamp,
            model,
            version,
          ),
        );
      }
    }
    // Test Results
    else if (artifact.body.artifact_type === "test_results") {
      if (isValidTestResults(artifact)) {
        testResults.value.push(
          new TableItem(
            artifact.header.identifier,
            artifact.header.timestamp,
            model,
            version,
            artifact.body.test_suite_id,
          ),
        );
      }
    }
    // Evidence
    else if (artifact.body.artifact_type === "evidence") {
      if (isValidEvidence(artifact)) {
        evidences.value.push(
          new TableItem(
            artifact.header.identifier,
            artifact.header.timestamp,
            model,
            version,
            undefined,
            artifact.body.metadata.measurement.measurement_class,
            artifact.body.value.evidence_type,
          ),
        );
      }
    }
  });
}

// Clear all Artifacts from local state.
function clearArtifacts() {
  negotiationCards.value = [];
  reports.value = [];
  testSuites.value = [];
  testResults.value = [];
  evidences.value = [];
}

/**
 * Save a new Model.
 *
 * @param {string} modelName Name of Model to be created
 */
async function createNewModel(modelName: string) {
  const response = await createModel(modelName);
  if (response) {
    populateModelList();
    successfulSubmission("Model", modelName, "created");
    newModelIdentifier.value = "";
    selectModel(modelName, true);
  }
}

/**
 * Save a new Version.
 *
 * @param {string} modelName Name of model to create new Version for.
 * @param {string} versionName Name of the new Version.
 */
async function submitNewVersion(modelName: string, versionName: string) {
  const response = await useApi("/model/" + modelName + "/version", "POST", {
    body: { identifier: versionName },
  });
  if (response) {
    selectModel(modelName, false);
    successfulSubmission("Version", versionName, "created");
    newVersionIdentifier.value = "";
    selectVersion(versionName);
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
