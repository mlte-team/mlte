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
          <UsaCheckbox
            v-for="model in modelOptions"
            :key="model"
            @update:modelValue="updateSelectedModels(model)"
          >
            {{ model }}
          </UsaCheckbox>
        </div>
        <br />
      </div>

      <div class="split-div">
        <b>Version(s)</b>
        <div class="scrollable-div">
          <UsaCheckbox
            v-for="version in versionOptions"
            :key="version"
            @update:modelValue="updateSelectedVersions(version)"
          >
            {{ version }}
          </UsaCheckbox>
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
          <UsaTable :headers="cardSpecReportHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Reports">
        <div class="scrollable-table-div">
          <UsaTable :headers="cardSpecReportHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Findings">
        <div class="scrollable-table-div">
          <UsaTable :headers="findingsHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Results">
        <div class="scrollable-table-div">
          <UsaTable :headers="resultsHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Values">
        <div class="scrollable-table-div">
          <UsaTable :headers="valuesHeaders" borderless class="table" />
        </div>
      </UsaAccordionItem>
    </UsaAccordion>
  </NuxtLayout>
</template>

<script setup>
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
]);

const namespaces = ref(["Default", "TEST 1", "Super longg purposes"]);

const selectedNamespace = ref("Default");
const newNamespaceFlag = ref(false);
const newNamespaceInput = ref("");

const modelOptions = ref([
  "model1",
  "model2",
  "model3",
  "model4",
  "model5",
  "model6",
  "model7",
  "model8",
]);
const selectedModels = ref([]);
const versionOptions = ref(["v1", "v2", "v3", "v4", "v5", "v6", "v1.5"]);
const selectedVersions = ref([]);
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

const negotiationCards = ref([
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
  { id: "test1", descriptor: "test1", date: "test1" },
]);

function selectNamespace(namespace) {
  // TODO : Send request to backend to get new info
  this.selectedNamespace = namespace;
}

async function addNamespace(namespace) {
  // TODO : Post this value to the backend so that it is validated.
  // TODO : Validate that submitted value isn't empty
  this.namespaces.push(namespace);
  this.newNamespaceFlag = false;
  this.newNamespaceInput = "";
  // const { data } = await useFetch("proxy/healthz");
  // this.namespaces.push(data)
}

function deleteNamespace(namespace) {
  // TODO : Post this value to the backend
  this.namespaces.splice(this.namespaces.indexOf(namespace), 1);
}

function updateSelectedModels(model) {
  // TODO : Post this to packend and get updated data
  const index = this.selectedModels.indexOf(model);
  if (index === -1) {
    this.selectedModels.push(model);
  } else {
    this.selectedModels.splice(index, 1);
  }
}

function updateSelectedVersions(version) {
  // TODO : Post this to packend and get updated data
  const index = this.selectedVersions.indexOf(version);
  if (index === -1) {
    this.selectedVersions.push(version);
  } else {
    this.selectedVersions.splice(index, 1);
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
