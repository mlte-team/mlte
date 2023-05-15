<template>
  <NuxtLayout name="base-layout">
    <template v-slot:sidebar>
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
    </template>

    <UsaBreadcrumb :items="path"/>

    <h1>{{ selected_namespace }}</h1>
    <hr/>

    <div style="margin-bottom: 2em;">
      <div class="inline-input-left">
        <UsaSelect v-model="selected_model" :options="model_options">
          <template v-slot:label>
            Model(s)
          </template>
        </UsaSelect>
      </div>

      <div class="inline-input-left">
        <UsaSelect v-model="selected_version" :options="version_options">
          <template v-slot:label>
            Version(s)
          </template>
        </UsaSelect>
      </div>

      <div class="inline-input-right">
        <UsaTextInput v-model="search_input">
          <template v-slot:label>
            Search
          </template>
        </UsaTextInput>
      </div>
    </div>

    <UsaAccordion multiselectable bordered>
      <UsaAccordionItem label="Negotiation Cards">
        <UsaTable
          :headers="card_spec_report_headers"
          caption="This is a description for the Negotiation Cards to assist..."
          borderless
          class="table"
        />
        <NuxtLink to="/negotiation-card">
          <UsaButton class="primary-button" style="float: right;">
            Start new negotiation card
          </UsaButton>
        </NuxtLink>
      </UsaAccordionItem>

      <UsaAccordionItem label="Specifications">
        <UsaTable
          :headers="card_spec_report_headers"
          borderless
          class="table"
        />
      </UsaAccordionItem>

      <UsaAccordionItem label="Reports">
        <UsaTable
          :headers="card_spec_report_headers"
          borderless
          class="table"
        />
      </UsaAccordionItem>

      <UsaAccordionItem label="Findings">
        <UsaTable
          :headers="findings_headers"
          borderless
          class="table"
        />
      </UsaAccordionItem>

      <UsaAccordionItem label="Results">
        <UsaTable
          :headers="results_headers"
          borderless
          class="table"
        />
      </UsaAccordionItem>

      <UsaAccordionItem label="Values">
        <UsaTable
          :headers="values_headers"
          borderless
          class="table"
        />
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
    "Default",
    "TEST 1",
    "Super longg purposes",
  ])

  var selected_namespace = ref("Default")
  var new_namespace_flag = ref(false)
  var new_namespace_input = ref("")

  var model_options = ref([
    {"value": "model1", "text": "model1"},
    {"value": "model2", "text": "model2"}
  ])
  var selected_model = ref("")
  var version_options = ref([
    {"value": "v1", "text": "v1"},
    {"value": "v2", "text": "v2"},
    {"value": "v3", "text": "v3"}
  ])
  var selected_version = ref("")
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


  function selectNamespace(namespace){
    // TODO : Send request to backend to get new info
    this.selected_namespace = namespace;
  }

  function addNamespace(namespace){
    // TODO : Post this value to the backend so that it is validated.
    this.namespaces.push(namespace);
    this.new_namespace_flag = false;
  }

  function deleteNamespace(namespace){
    // TODO : Post this value to the backend
    this.namespaces.splice(this.namespaces.indexOf(namespace), 1)
  }
</script>

<style>
.table {
  width: 100%;
}
</style>