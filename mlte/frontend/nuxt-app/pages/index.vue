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
        <b>Model(s)</b>
        <div class="scrollable-div">
          <div v-for="entry in modelOptions" :key="entry.model">
            <ScrollableListItem
              :selected="entry.selected"
              @update="updateSelectedModels(entry)"
              @delete="deleteModel(entry)"
            >
              {{ entry.model }}
            </ScrollableListItem>
          </div>
        </div>
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
          <UsaTable
            :headers="cardSpecReportHeaders"
            :rows="negotiationCards"
            borderless
            class="table"
          />
          <!-- TODO : This will have to be more info than the namespace. Probably model version -->
          <NuxtLink
            :to="{
              path: 'negotiation-card',
              query: { namespace: selectedNamespace },
            }"
          >
            <UsaButton class="primary-button" style="float: right">
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
          <UsaTable
            :headers="cardSpecReportHeaders"
            :rows="reports"
            borderless
            class="table"
          />
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
if (namespaceOptions.value !== null && namespaceOptions.value.length > 0) {
  selectNamespace(namespaceOptions.value[0]);
}
const newNamespaceFlag = ref(false);
const newNamespaceInput = ref("");

const modelOptions = ref<{ model: string; selected: boolean }[]>([]);
const versionOptions = ref<
  { model: string; version: string; selected: boolean }[]
>([]);
// const searchInput = ref("");

const cardSpecReportHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

const validatedSpecHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "specid", label: "SpecID", sortable: true },
  { id: "timestamp", label: "Timestamp", sortable: true },
]);

// const resultsHeaders = ref([
//   { id: "id", label: "ID", sortable: true },
//   { id: "value", label: "value", sortable: true },
//   { id: "condition", label: "Condition", sortable: true },
//   { id: "outcome", label: "Outcome", sortable: true },
//   { id: "Date", label: "Date", sortable: true },
// ]);

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

        response._data.forEach((modelName: string) => {
          if (!modelOptions.value.some((item) => item.model === modelName)) {
            modelOptions.value.push({ model: modelName, selected: false });
          }
        });

        modelOptions.value.sort((a, b) => a.model.localeCompare(b.model));
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
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
}

async function updateSelectedVersions(entry: {
  model: string;
  version: string;
  selected: boolean;
}) {
  // TODO : Ideally this would be handled with the prop of the component
  entry.selected = !entry.selected;

  // TODO : Post this to backend and get updated data
  if (entry.selected) {
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
        },
        onResponseError() {
          responseErrorAlert();
        },
      },
    );
  }
}

function requestErrorAlert() {
  alert(
    "Error encountered while communicating with API. Ensure store is running and allowed-origins is configured correctly.",
  );
}

function responseErrorAlert() {
  alert(
    "Error encountered in response from API. Check browser and store console for more information.",
  );
}

function addSelectedArtifacts(model: string, version: string, artifactList){
  artifactList.forEach(artifact => {
    // negotiation card
    // if(artifact.header.type == "negotiation"){
    //   if(isValidNegotiation(artifact)){
    //     negotiationCards.value.push(
    //       {
    //         id: artifact.header.identifier,
    //         timestamp: new Date(artifact.header.timestamp * 1000).toString(),
    //         model: model,
    //         version: version
    //       }
    //     )
    //   }
    // }
    // report
    // else if(artifact.header.type == "report"){
    //   if(isValidReport(artifact)){
    //     reports.value.push(
    //       {
    //         id: artifact.header.identifier,
    //         timestamp: new Date(artifact.header.timestamp * 1000).toString(),
    //         model: model,
    //         version: version
    //       }
    //     )
    //   }
    // }
    // spec
    if(artifact.header.type == "3"){
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
    else if(artifact.header.type == "4"){
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
    if(artifact.header.type == "2") {
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
  // TODO : negotiationCards.value = 
  // TODO : reports.value = 
  specifications.value = specifications.value.filter(function (spec) {
    return spec.model !== model || spec.version !== version;
  });

  validatedSpecs.value = validatedSpecs.value.filter(function (validatedSpec) {
    return validatedSpec.model !== model || validatedSpec.version !== version;
  });

  values.value = values.value.filter(function (value) {
    return value.model !== model || value.version !== version;
  });
}
</script>

<style>
.scrollable-table-div {
  overflow-y: auto;
  height: 14em;
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
