<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 115px">
        Namespaces
        <hr />
        <div v-for="namespaceName in namespaces" :key="namespaceName">
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
          <div v-for="model in modelOptions">
            <ScrollableListItem
              @update="updateSelectedModels(model)"
              @delete="deleteModel(model)"
            >
              {{ model }}
            </ScrollableListItem>
          </div>
        </div>
        <br />
      </div>

      <div class="split-div">
        <b>Version(s)</b>
        <div class="scrollable-div">
          <div v-for="option in versionOptions">
            <ScrollableListItem
              @update="updateSelectedVersions(option.version)"
              @delete="deleteVersion(option.version)"
            >
              {{ option.model }} - {{ option.version }}
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

      <UsaAccordionItem label="Specifications">
        <div class="scrollable-table-div">
          <p>
            A specification (spec) defines the model requirements that must be
            satisfied to ensure successful integration with the target system.
          </p>
          <UsaTable :headers="cardSpecReportHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Reports">
        <div class="scrollable-table-div">
          <p>
            A report is a human and machine-readable summary of all knowledge
            gained about a model during the MLTE process.
          </p>
          <UsaTable :headers="cardSpecReportHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Findings">
        <div class="scrollable-table-div">
          <p>
            Findings are produced by combining a specification with its
            corresponding results; this artifact communicates how well a model
            performed against all of its requirements.
          </p>
          <UsaTable :headers="findingsHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Results">
        <div class="scrollable-table-div">
          <p>
            Results encode whether or not the values generated during evidence
            collection pass their corresponding validation threshold. They are
            produced by feeding values through the relevant condition callbacks
            provided in the MLTE specification.
          </p>
          <UsaTable :headers="resultsHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Values">
        <div class="scrollable-table-div">
          <p>
            Values are the atomic unit of model evaluation in MLTE. A value is
            any artifact produced by a MLTE measurement for the purposes of
            model evaluation.
          </p>
          <UsaTable :headers="valuesHeaders" borderless class="table" />
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

var { data: namespaces } = await useFetch("api/namespace", { method: "GET" });
const selectedNamespace = ref("Default");
const newNamespaceFlag = ref(false);
const newNamespaceInput = ref("");

const modelOptions = ref<string[]>([]);
const selectedModels = ref<string[]>([]);
const versionOptions = ref<{model: string, version: string}[]>([]);
const selectedVersions = ref<string[]>([]);
// const searchInput = ref("");

const cardSpecReportHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "descriptor", label: "Descriptor", sortable: true },
  { id: "date", label: "Date", sortable: true },
]);

const findingsHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "date", label: "Date", sortable: true },
  { id: "spec", label: "Spec", sortable: true },
]);

const resultsHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "value", label: "value", sortable: true },
  { id: "condition", label: "Condition", sortable: true },
  { id: "outcome", label: "Outcome", sortable: true },
  { id: "Date", label: "Date", sortable: true },
]);

const valuesHeaders = ref([
  { id: "id", label: "ID", sortable: true },
  { id: "measurement", label: "Measurement", sortable: true },
  { id: "type", label: "Type", sortable: true },
  { id: "date", label: "Date", sortable: true },
]);

const negotiationCards = ref([]);

async function selectNamespace(namespace: string) {
  selectedNamespace.value = namespace;
  const { data } = await useFetch<string[] | null>("api/namespace/" + namespace + "/model", { method: "GET" });
  modelOptions.value = data.value !== null ? data.value : [];
  versionOptions.value = []
}

async function addNamespace(namespace: string) {
  if(namespace != ""){
    await useFetch("api/namespace", {
      method: "POST",
      body: { 
        identifier: namespace,
      }
    });
    // TODO : Error handling

    const { data } = useFetch("api/namespace", { method: "GET" })
    namespaces = data;
    newNamespaceFlag.value = false;
    newNamespaceInput.value = "";
  }
}

async function deleteNamespace(namespace: string) {
  // TODO : Add confirm

  // TODO : Post this value to the backend
  // namespaces.value.splice(namespaces.value.indexOf(namespace), 1);

  // await useFetch("/api/namespace/" + namespace, {
  //   method: 'DELETE',
  // }).then(() => console.log('request happened ig'));
  // TODO : Error handling

  // const { data, error } = await useFetch("http://localhost:8080/api/namespace/" + namespace, {
  //   method: 'DELETE',
  // });
  const { data, error } = await useFetch("api/namespace/" + namespace, {
    method: 'DELETE',
  });
  console.log(data);
  console.log(error);


  // const response = await fetch('https://testapi.jasonwatmore.com/products/1', { method: 'DELETE' });
  // const data = await response.json();  

  // const response = await fetch('/test/', { method: 'DELETE' });
  // const data = await response.json();

  // await fetch('/api/namespace/test', { method: 'DELETE' });
}

async function deleteModel(model: string){
  // TODO : Add confirm
  const { data, error } = await useFetch("api/namespace/" + selectedNamespace.value + "/model/" + model, {
    method: 'DELETE',
  });
  console.log(data);
  console.log(error);
  // TODO : Error handling

  console.log("model deleted xd");
  console.log(model)
}

async function deleteVersion(version: string){
  // TODO : Add confirm
  // const { data, error } = await useFetch("api/namespace/" + selectedNamespace.value + "/model/" + model, {
  //   method: 'DELETE',
  // });
  // console.log(data);
  // console.log(error);
  // TODO : Error handling

  console.log("version deleted xd");
  console.log(version)
}

async function updateSelectedModels(model: string) {
  const index = selectedModels.value.indexOf(model);
  if (index === -1) {
    selectedModels.value.push(model);
    const { data: versions } = await useFetch<string[]>("api/namespace/" + selectedNamespace.value + "/model/" + model + "/version");
    if(versions.value){
      versions.value.forEach(version => {
        versionOptions.value.push({'model': model, 'version': version})
      })
    }
  } else {
    versionOptions.value = versionOptions.value.filter(function (version: string) {
      return version.substring(0, model.length) != model
    })

    selectedModels.value.splice(index, 1);
  }

  versionOptions.value.sort();
}

function updateSelectedVersions(version: string) {
  // TODO : Post this to backend and get updated data
  const index = selectedVersions.value.indexOf(version);
  if (index === -1) {
    selectedVersions.value.push(version);
  } else {
    selectedVersions.value.splice(index, 1);
  }
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
