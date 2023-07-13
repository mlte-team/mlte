<template>
  <NuxtLayout name="base-layout">
    <template v-slot:sidebar>
      <div style="padding-top: 115px;">
        Namespaces
        <hr/>
        <div v-for="(namespace, index) in namespaces">
          <SidebarItem
            @select="selectNamespace(namespace)"  
            @delete="deleteNamespace(namespace)"
          >
            {{ namespace }}
          </SidebarItem>
        </div>
        
        <AddButton v-if="!new_namespace_flag" @click="new_namespace_flag = true"/>
        <UsaTextInput
          v-if="new_namespace_flag"
          v-model="new_namespace_input"
          @keyup.enter="addNamespace(new_namespace_input)"
        />
      </div>
    </template>

    <UsaBreadcrumb :items="path"/>

    <h1>{{ selected_namespace }}</h1>
    <hr/>

    <div style="display: flex">
      <div class="split-div">
        <b>Model(s)</b>
        <div class="scrollable-div">
          <UsaCheckbox v-for="(model) in model_options" @update:modelValue="updateSelectedModels(model)">
            {{ model }}
          </UsaCheckbox>
        </div>
        <br/>
      </div>

      <div class="split-div">
        <b>Version(s)</b>
        <div class="scrollable-div">
          <UsaCheckbox v-for="(version) in version_options" @update:modelValue="updateSelectedVersions(version)">
            {{ version }}
          </UsaCheckbox>
        </div>
        <br/>
      </div>

      <div>
        <!-- Placeholder for when the search functionality is implemented
        <label class="usa-label" style="margin-top: 0px;">Search</label>
        <UsaTextInput v-model="search_input" style="width: 100%;"/> -->
      </div>
    </div>

    <UsaAccordion multiselectable bordered>
      <UsaAccordionItem label="Negotiation Cards">
        <div class="scrollable-table-div">
          <UsaTable
            :headers="card_spec_report_headers"
            :rows="negotiation_cards"
            borderless
            class="table"
          />
          <!-- TODO : This will have to be more info than the namespace. Probably model version -->
          <NuxtLink :to="{path: 'negotiation-card', query: {namespace: selected_namespace}}">
            <UsaButton class="primary-button" style="float: right;">
              Start new negotiation card
            </UsaButton>
          </NuxtLink>
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Specifications">
        <div class="scrollable-table-div">
          <UsaTable
            :headers="card_spec_report_headers"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Reports">
        <div class="scrollable-table-div">
          <UsaTable
            :headers="card_spec_report_headers"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Findings">
        <div class="scrollable-table-div">
          <UsaTable
            :headers="findings_headers"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Results">
        <div class="scrollable-table-div">
          <UsaTable
            :headers="results_headers"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>

      <UsaAccordionItem label="Values">
        <div class="scrollable-table-div">
          <UsaTable
            :headers="values_headers"
            borderless
            class="table"
          />
        </div>
      </UsaAccordionItem>
    </UsaAccordion>
  </NuxtLayout>
</template>
  
<script setup>
  var path = ref([
    {
      "href": "/",
      "text": "Artifact Store"
    }
  ])

  var namespaces = ref([
    "Default", "TEST 1", "Super longg purposes",
  ])

  var selected_namespace = ref("Default")
  var new_namespace_flag = ref(false)
  var new_namespace_input = ref("")

  var model_options = ref([
    "model1", "model2", "model3", "model4", "model5", "model6", "model7", "model8"
  ])
  var selected_models = ref([])
  var version_options = ref([
    "v1", "v2", "v3", "v4", "v5", "v6", "v1.5"
  ])
  var selected_versions = ref([])
  var search_input = ref("")

  var card_spec_report_headers = ref([
    {"id": "id", "label": "ID", "sortable": true},
    {"id": "descriptor", "label": "Descriptor", "sortable": true},
    {"id": "date", "label": "Date", "sortable": true},
  ])

  var findings_headers = ref([
    {"id": "id", "label": "ID", "sortable": true},
    {"id": "date", "label": "Date", "sortable": true},
    {"id": "spec", "label": "Spec", "sortable": true},
  ])

  var results_headers = ref([
    {"id": "id", "label": "ID", "sortable": true},
    {"id": "value", "label": "value", "sortable": true},
    {"id": "condition", "label": "Condition", "sortable": true},
    {"id": "outcome", "label": "Outcome", "sortable": true},
    {"id": "Date", "label": "Date", "sortable": true},
  ])

  var values_headers = ref([
    {"id": "id", "label": "ID", "sortable": true},
    {"id": "measurement", "label": "Measurement", "sortable": true},
    {"id": "type", "label": "Type", "sortable": true},
    {"id": "date", "label": "Date", "sortable": true},
  ])

  var negotiation_cards = ref([
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"},
  {"id": "test1", "descriptor": "test1", "date": "test1"}
  ])


  function selectNamespace(namespace){
    // TODO : Send request to backend to get new info
    this.selected_namespace = namespace;
  }

  async function addNamespace(namespace){
    // TODO : Post this value to the backend so that it is validated.
    // TODO : Validate that submitted value isn't empty
    this.namespaces.push(namespace);
    this.new_namespace_flag = false;
    this.new_namespace_input = ""
    // const { data } = await useFetch("proxy/healthz");
    // this.namespaces.push(data)
  }

  function deleteNamespace(namespace){
    // TODO : Post this value to the backend
    this.namespaces.splice(this.namespaces.indexOf(namespace), 1)
  }

  function updateSelectedModels(model){
    // TODO : Post this to packend and get updated data
    var index = this.selected_models.indexOf(model)
    if(index == -1){
      this.selected_models.push(model)
    }
    else{
      this.selected_models.splice(index, 1)
    }
  }

  function updateSelectedVersions(version){
    // TODO : Post this to packend and get updated data
    var index = this.selected_versions.indexOf(version)
    if(index == -1){
      this.selected_versions.push(version)
    }
    else{
      this.selected_versions.splice(index, 1)
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

.scrollable-div{
  border: 1px solid gray;
  overflow-y: auto;
  height: 11em;
  padding-left: .4em;
}
</style>