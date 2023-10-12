<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 115px">
        Namespaces
        <hr />
        <div v-for="namespaceName in namespaceOptions" :key="namespaceName">
          <SidebarItem
            @select="selectNamespace(namespaceName)"
            @delete="deleteNamespace(namespaceName)"
          >
            {{ namespaceName }}
          </SidebarItem>
        </div>

        <AddButton v-if="!newNamespaceFlag" @click="newNamespaceFlag = true" />
        <UsaTextInput
          v-if="newNamespaceFlag"
          v-model="newNamespaceInput"
          @keyup.enter="addNamespace(newNamespaceInput)"
          @keyup.escape="newNamespaceFlag = false"
        />
      </div>
    </template>

    <UsaBreadcrumb :items="path" />

    <h1>{{ selectedNamespace }}</h1>
    <hr />

    <div style="display: flex">
      
      <div class="split-div">
        <b>New Model(s)</b>
        <UsaSelect 
          :options=modelOptions
          @update:modelValue=myUpdateSelectedModels({})
        />
      <br />
      </div>

      <div class="split-div">
        <b>Version(s)</b>
        <div class="scrollable-div">
          <div v-for="entry in versionOptions" :key="entry.version">
            <ScrollableListItem
              :selected="entry.selected"
              @update="updateSelectedVersions(entry)"
              @delete="deleteVersion(entry)"
            >
              {{ entry.model }} - {{ entry.version }}
            </ScrollableListItem>
          </div>
        </div>
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
          <!-- <UsaTable
            :headers="cardSpecReportHeaders"
            :rows="negotiationCards"
            borderless
            class="table"
          /> -->
          <table class="table usa-table usa-table--borderless">
            <thead>
              <tr>
                <th data-sortable scope="col" role="columnheader">ID</th>
                <th data-sortable scope="col" role="columnheader">Timestamp</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="card in negotiationCards">
                <th scope="row">{{ card.id }}</th>
                <td>{{ card.timestamp }}</td>
                <td>
                  <NuxtLink
                    :to="{
                      path: 'negotiation-card',
                      query: { namespace: selectedNamespace, model: card.model, version: card.version, artifactId: card.id },
                    }"
                  >
                    <UsaButton class="primary-button">
                      Edit
                    </UsaButton>
                  </NuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
          <!-- TODO : Adjust this once a mode/version selector is implemented -->
          <p v-if="selectedVersion == ''" style="float: left; color: red;">
            Select a model version in order to start a new negotiation card
          </p>
          <NuxtLink
            :to="{
              path: 'negotiation-card',
              query: { namespace: selectedNamespace, model: selectedModel, version: selectedVersion },
            }"
          >
            <UsaButton :disabled="selectedVersion == ''" class="primary-button" style="float: right">
              Start new negotiation card
            </UsaButton>
          </NuxtLink>
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Reports">
        <div class="scrollable-table-div">
          <p>
            A report is a human and machine-readable summary of all knowledge
            gained about a model during the MLTE process.
          </p>
          <!-- <UsaTable
            :headers="cardSpecReportHeaders"
            :rows="reports"
            borderless
            class="table"
          /> -->
          <table class="table usa-table usa-table--borderless">
            <thead>
              <tr>
                <th data-sortable scope="col" role="columnheader">ID</th>
                <th data-sortable scope="col" role="columnheader">Timestamp</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in reports">
                <th scope="row">{{ report.id }}</th>
                <td>{{ report.timestamp }}</td>
                <td>
                  <NuxtLink
                    :to="{
                      path: 'report',
                      query: { namespace: selectedNamespace, model: report.model, version: report.version, arfifactId: report.id },
                    }"
                  >
                    <UsaButton class="primary-button">
                      Edit
                    </UsaButton>
                  </NuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
          <!-- TODO : Adjust this once a mode/version selector is implemented -->
          <p v-if="selectedVersion == ''" style="float: left; color: red;">
            Select a model version in order to start a new report
          </p>
          <NuxtLink
            :to="{
              path: 'report',
              query: { namespace: selectedNamespace, model: selectedModel, version: selectedVersion },
            }"
          >
            <UsaButton :disabled="selectedVersion == ''" class="primary-button" style="float: right">
              Start new report
            </UsaButton>
          </NuxtLink>
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
            Validated Specification are produced by combining a specification with its
            corresponding results; this artifact communicates how well a model
            performed against all of its requirements.
          </p>
          <UsaTable
            :headers="validatedSpecHeaders"
            :rows="validatedSpecs"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <!-- <UsaAccordionItem label="Results">
        <div class="scrollable-table-div">
          <p>
            Results encode whether or not the values generated during evidence
            collection pass their corresponding validation threshold. They are
            produced by feeding values through the relevant condition callbacks
            provided in the MLTE specification.
          </p>
          <UsaTable :headers="resultsHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem> -->

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
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
]);

const { data: namespaceOptions } = await useFetch<string[]>(
  "http://localhost:8080/api/namespace",
  { method: "GET" },
);
const selectedNamespace = ref("");
// TODO : Remove these once a mode/version selector is implemented
const selectedModel = ref("");
const selectedVersion = ref("");
// -- end block to be removed

if (namespaceOptions.value !== null && namespaceOptions.value.length > 0) {
  selectNamespace(namespaceOptions.value[0]);
}
const newNamespaceFlag = ref(false);
const newNamespaceInput = ref("");

const modelOptions = ref<{ value: int; text: string }[]>([])
const versionOptions = ref<
  { model: string; version: string; selected: boolean }[]
>([]);


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
  { id: string; timestamp: string, model: string, version: string }[]
>([]);
const reports = ref<
  { id: string; timestamp: string; model: string; version: string }[]
>([]);
const validatedSpecs = ref<
  { id: string; specid: string; timestamp: string, model: string, version: string }[]
>([]);
const values = ref<
  { id: string; measurement: string; type: string; timestamp: string, model: string, version: string }[]
>([]);

async function selectNamespace(namespace: string) {
  await useFetch(
    "http://localhost:8080/api/namespace/" + namespace + "/model",
    {
      retry: 0,
      method: "GET",
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (selectedNamespace.value !== namespace) {
          selectedNamespace.value = namespace;
          modelOptions.value = [];
          versionOptions.value = [];
        }

        response._data.forEach((modelName: string, index: int) => {
          if (!modelOptions.value.some((item) => item.model === modelName)) {
            modelOptions.value.push({ value: index, text: modelName });
          }
        });

        modelOptions.value.sort((a, b) => a.text.localeCompare(b.text));

        negotiationCards.value = [];
        reports.value = [];
        specifications.value = [];
        validatedSpecs.value = [];
        values.value = [];
      },
      onResponseError() {
        responseErrorAlert();
      },
    },
  );
}

async function addNamespace(namespace: string) {
  if (namespace !== "") {
    const { error } = await useFetch("http://localhost:8080/api/namespace", {
      retry: 0,
      method: "POST",
      body: {
        identifier: namespace,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponseError() {
        responseErrorAlert();
      },
    });

    if (error.value === null) {
      await useFetch("http://localhost:8080/api/namespace", {
        method: "GET",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          namespaceOptions.value =
            response._data !== null ? response._data : [];
          newNamespaceFlag.value = false;
          newNamespaceInput.value = "";
        },
        onResponseError() {
          responseErrorAlert();
        },
      });
    }
  }
}

async function deleteNamespace(namespace: string) {
  if (
    confirm("Are you sure you want to delete the namespace: " + namespace + "?")
  ) {
    const { error } = await useFetch(
      "http://localhost:8080/api/namespace/" + namespace,
      {
        retry: 0,
        method: "DELETE",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }){
          negotiationCards.value = [];
          reports.value = [];
          specifications.value = [];
          validatedSpecs.value = [];
          values.value = [];
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );

    if (error.value === null) {
      await useFetch("http://localhost:8080/api/namespace", {
        retry: 0,
        method: "GET",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          namespaceOptions.value =
            response._data !== null ? response._data : [];
        },
        onResponseError() {
          responseErrorAlert();
        },
      });
    }
  }

  // Reselecting the top listed namespace if the one that was selected is the one that is being deleted
  if (selectedNamespace.value === namespace) {
    selectedNamespace.value =
      namespaceOptions.value !== null ? namespaceOptions.value[0] : "";
    if (selectedNamespace.value !== "") {
      selectNamespace(selectedNamespace.value);
    }
  }
}

async function updateSelectedModels(entry: {
  model: string;
  selected: boolean;
}) {
  // TODO : Ideally this would be handled with the prop of the component
  entry.selected = !entry.selected;

  if (entry.selected) {
    await useFetch(
      "http://localhost:8080/api/namespace/" +
        selectedNamespace.value +
        "/model/" +
        entry.model +
        "/version",
      {
        retry: 0,
        method: "GET",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          if (response._data) {
            response._data.forEach((version: string) => {
              versionOptions.value.push({
                model: entry.model,
                version,
                selected: false,
              });
            });
          }
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  } else {
    versionOptions.value = versionOptions.value.filter(function (versionItem: {
      model: string;
      version: string;
    }) {
      return versionItem.model !== entry.model;
    });
    clearDeselectedArtifacts(entry.model, "");
  }

  versionOptions.value.sort(function (
    a: { model: string; version: string },
    b: { model: string; version: string },
  ) {
    if (a.model < b.model) {
      return -1;
    } else if (a.model > b.model) {
      return 1;
    } else if (a.model === b.model) {
      if (a.version < b.version) {
        return -1;
      } else {
        return 1;
      }
    }
    return 0;
  });
}

async function myUpdateSelectedModels(event) {
  console.log(event)
}

/*
async function deleteModel(entry: { model: string; selected: boolean }) {
  if (
    confirm("Are you sure you want to delete the model: " + entry.model + "?")
  ) {
    await useFetch(
      "http://localhost:8080/api/namespace/" +
        selectedNamespace.value +
        "/model/" +
        entry.model,
      {
        retry: 0,
        method: "DELETE",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse() {
          const index = modelOptions.value.indexOf(entry);
          modelOptions.value.splice(index, 1);
          updateSelectedModels(entry);
          negotiationCards.value = [];
          reports.value = [];
          specifications.value = [];
          validatedSpecs.value = [];
          values.value = [];
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
}
*/

async function updateSelectedVersions(entry: {
  model: string;
  version: string;
  selected: boolean;
}) {
  // TODO : Ideally this would be handled with the prop of the component
  entry.selected = !entry.selected;

  if (entry.selected) {
    // TODO : Remove this block once a mode/version selector is implemented
    // Block handles updating artifacts when a second version is selected.
    // This implementation makes only one selectable at a time.
    // When removed, also update start new negotiation card and start new report button,
    // remove the global selectedModel and selectedVersion values, and adjust the else
    // block after this if
    versionOptions.value.forEach((version) => {
      negotiationCards.value = [];
      reports.value = [];
      specifications.value = [];
      validatedSpecs.value = [];
      values.value = [];
      version.selected = false;
    })
    entry.selected = true;
    selectedModel.value = entry.model;
    selectedVersion.value = entry.version;
    // -- end block to be removed

    await useFetch(
      "http://localhost:8080/api/namespace/" +
        selectedNamespace.value +
        "/model/" +
        entry.model +
        "/version/" +
        entry.version +
        "/artifact",
      {
        retry: 0,
        method: "GET",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          if (response._data) {
            addSelectedArtifacts(entry.model, entry.version, response._data);
          }
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
  else{
    clearDeselectedArtifacts(entry.model, entry.version);

    // TODO : Remove this block once a mode/version selector is implemented
    selectedModel.value = "";
    selectedVersion.value = "";
    // -- end block to be removed
  }
}

async function deleteVersion(entry: {
  model: string;
  version: string;
  selected: boolean;
}) {
  if (
    confirm(
      "Are you sure you want to delete the version: " +
        entry.model +
        " - " +
        entry.version +
        "?",
    )
  ) {
    await useFetch(
      "http://localhost:8080/api/namespace/" +
        selectedNamespace.value +
        "/model/" +
        entry.model +
        "/version/" +
        entry.version,
      {
        retry: 0,
        method: "DELETE",
        onRequestError() {
          requestErrorAlert();
        },
        onResponse() {
          const index = versionOptions.value.indexOf(entry);
          versionOptions.value.splice(index, 1);
          clearDeselectedArtifacts(entry.model, entry.version);
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
}

// TODO : Do better typing on the artifactList and artifact
function addSelectedArtifacts(model: string, version: string, artifactList: any){
  artifactList.forEach((artifact: any) => {
    // negotiation card
    if(artifact.header.type == "negotiation_card"){
      if(isValidNegotiation(artifact)){
        negotiationCards.value.push(
          {
            id: artifact.header.identifier,
            timestamp: new Date(artifact.header.timestamp * 1000).toString(),
            model: model,
            version: version
          }
        )
      }
    }
    // report
    else if(artifact.header.type == "report"){
      if(isValidReport(artifact)){
        reports.value.push(
          {
            id: artifact.header.identifier,
            timestamp: new Date(artifact.header.timestamp * 1000).toString(),
            model: model,
            version: version
          }
        )
      }
    }
    // spec
    else if(artifact.header.type == "spec"){
      if(isValidSpec(artifact)){
        specifications.value.push(
          {
            id: artifact.header.identifier,
            timestamp: new Date(artifact.header.timestamp * 1000).toString(),
            model: model,
            version: version
          }
        )
      }
    }
    // validated spec
    else if(artifact.header.type == "validated_spec"){
      if(isValidValidatedSpec(artifact)){
        validatedSpecs.value.push(
          {
            id: artifact.header.identifier,
            specid: artifact.body.spec_identifier,
            timestamp: new Date(artifact.header.timestamp * 1000).toString(),
            model: model,
            version: version
          }
        )
      }
    }
    // value
    if(artifact.header.type == "value") {
      if(isValidValue(artifact)){
        values.value.push(
          {
            id: artifact.header.identifier.slice(0, -6),
            measurement: artifact.body.metadata.measurement_type,
            type: artifact.body.value.value_type,
            timestamp: new Date(artifact.header.timestamp * 1000).toString(),
            model: model,
            version: version
          }
        )
      } 
    }
  });
}

function clearDeselectedArtifacts(model: string, version: string){
  // Passing a version causes both model and version to be checked before filtering items
  // If an empty string is passed as the version, all artifacts under the model will be filtered out

  negotiationCards.value = specifications.value.filter(function (card) {
    if(version === ""){
      return card.model !== model;
    }
    else{
      return card.model !== model || card.version !== version;
    }
  });

  reports.value = specifications.value.filter(function (report) {
    if(version === ""){
      return report.model !== model;
    }
    else{
      return report.model !== model || report.version !== version;
    }
  });

  specifications.value = specifications.value.filter(function (spec) {
    if(version === ""){
      return spec.model !== model
    }
    else{
      return spec.model !== model || spec.version !== version;
    }
  });

  validatedSpecs.value = validatedSpecs.value.filter(function (validatedSpec) {
    if(version === ""){
      return validatedSpec.model !== model
    }
    else{
      return validatedSpec.model !== model || validatedSpec.version !== version;
    }
  });

  values.value = values.value.filter(function (value) {
    if(version === ""){
      return value.model !== model
    }
    else{
      return value.model !== model || value.version !== version;
    }
  });
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

.split-div {
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
