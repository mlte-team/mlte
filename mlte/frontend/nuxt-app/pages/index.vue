<template>
  <NuxtLayout name="base-layout">
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
          @update:modelValue="selectModel($event, true)"
        >
        <template #label>Model</template>
      </UsaSelect>
        <br />
      </div>

      <div class="model-version-div">
        <UsaSelect
          :options="versionOptions"
          :model-value="selectedVersion"
          @update:modelValue="selectVersion($event)"
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

      <UsaAccordionItem label="Specifications">
        <div class="scrollable-table-div">
          <p>
            A specification (spec) defines the model requirements that must be
            satisfied to ensure successful integration with the target system.
          </p>
          <UsaTable
            :headers="cardSpecReportHeaders"
            :rows="specifications"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Validated Specification">
        <div class="scrollable-table-div">
          <p>
            Validated Specification are produced by combining a specification
            with its corresponding results; this artifact communicates how well
            a model performed against all of its requirements.
          </p>
          <UsaTable
            :headers="validatedSpecHeaders"
            :rows="validatedSpecs"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Values">
        <div class="scrollable-table-div">
          <p>
            Values are the atomic unit of model evaluation in MLTE. A value is
            any artifact produced by a MLTE measurement for the purposes of
            model evaluation.
          </p>
          <UsaTable
            :headers="valuesHeaders"
            :rows="values"
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
const path = ref([
  {
    href: "/",
    text: "",
  },
]);

const newModelIdentifier = ref("");
const newVersionIdentifier = ref("");

const modelOptions = ref<{ value: string; text: string }[]>([]);
const versionOptions = ref<{ value: string; text: string }[]>([]);
const modelList = ref<string[]>([]);

const selectedModel = useCookie("selectedModel", {
  decode: false,
});
selectedModel.value = selectedModel.value || "";
const selectedVersion = useCookie("selectedVersion", {
  decode: false,
});
selectedVersion.value = selectedVersion.value || "";

const cardSpecReportHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const validatedSpecHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "specid", label: "SpecID", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const valuesHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "measurement", label: "Measurement", sortable: true },
  { id: "type", label: "Type", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const negotiationCards = ref<
  { id: string; timestamp: string; model: string; version: string }[]
>([]);
const specifications = ref<
  { id: string; timestamp: string; model: string; version: string }[]
>([]);
const reports = ref<
  { id: string; timestamp: string; model: string; version: string }[]
>([]);
const validatedSpecs = ref<
  {
    id: string;
    specid: string;
    timestamp: string;
    model: string;
    version: string;
  }[]
>([]);
const values = ref<
  {
    id: string;
    measurement: string;
    type: string;
    timestamp: string;
    model: string;
    version: string;
  }[]
>([]);

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
  if (versionName === "") {
    clearArtifacts();
    return;
  }

  await $fetch(
    config.public.apiPath +
      "/model/" +
      selectedModel.value +
      "/version/" +
      versionName +
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
          selectedVersion.value = versionName;
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
// TODO : Do better typing on the artifactList and artifact
function populateArtifacts(
  model: string,
  version: string,
  artifactList: Array<object>,
) {
  clearArtifacts();
  artifactList.forEach((artifact: object) => {
    artifact.header.timestamp = new Date(
      artifact.header.timestamp * 1000,
    ).toLocaleString("en-US");
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
    // Spec
    else if (artifact.header.type === "spec") {
      if (isValidSpec(artifact)) {
        specifications.value.push({
          id: artifact.header.identifier,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
    // Validated spec
    else if (artifact.header.type === "validated_spec") {
      if (isValidValidatedSpec(artifact)) {
        validatedSpecs.value.push({
          id: artifact.header.identifier,
          specid: artifact.body.spec_identifier,
          timestamp: artifact.header.timestamp,
          model,
          version,
        });
      }
    }
    // Value
    if (artifact.header.type === "value") {
      if (isValidValue(artifact)) {
        values.value.push({
          id: artifact.header.identifier.slice(0, -6),
          measurement: artifact.body.metadata.measurement_type,
          type: artifact.body.value.value_type,
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
  specifications.value = [];
  validatedSpecs.value = [];
  values.value = [];
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
  } catch {}
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
  } catch {}
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
