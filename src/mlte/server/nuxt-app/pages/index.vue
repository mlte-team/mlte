<template>
  <NuxtLayout name="base-layout">
    <UsaAccordion multiselectable bordered>
      <UsaAccordionItem label="Negotiation Cards">
        <UsaTable
          :headers="card_spec_report_headers"
          caption="This is a description for the Negotiation Cards to assist..."
          borderless
          class="table"
        />
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
</script>

<style>
.table {
  width: 100%;
}
</style>