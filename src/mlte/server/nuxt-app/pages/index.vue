<template>
  <NuxtLayout name="base-layout">
    <UsaAccordion multiselectable bordered>
      <UsaAccordionItem>
        <template v-slot:label>
          <div class="section-header">
            Your Negotiation Cards         
          </div>
        </template>
        <UsaTable
          :headers="head"
          :rows="rows"
          caption="This is a description for the Negotiation Cards to assist..."
          borderless
          class="table"
        />
      </UsaAccordionItem>
      <UsaAccordionItem label="Specifications">Specifications</UsaAccordionItem>
      <UsaAccordionItem label="Reports">Reports</UsaAccordionItem>
      <UsaAccordionItem label="Findings">Findings</UsaAccordionItem>
      <UsaAccordionItem label="Results">Results</UsaAccordionItem>
      <UsaAccordionItem label="Values">Values</UsaAccordionItem>
    </UsaAccordion>
  </NuxtLayout>
</template>
  
<script setup>
  var head = ref([
    {
      "id": "alphabetical",
      "label": "Alphabetical",
      "sortable": false,
      "headerRow": true
    },
    {
      "id": "month",
      "label": "Month",
      "sortable": true
    },
    {
      "id": "percent",
      "label": "Percent",
      "sortable": true
    },
    {
      "id": "count",
      "label": "Count",
      "sortable": true
    }
  ])

  var rows = ref([
    {
      "alphabetical": "Tango",
      "month": {
        "sortValue": 3,
        "displayValue": "March"
      },
      "percent": {
        "sortValue": 0.206,
        "displayValue": "20.6%"
      },
      "count": {
        "sortValue": 23612,
        "displayValue": "23,612"
      }
    },
    {
      "alphabetical": "Foxtrot",
      "month": {
        "sortValue": 4,
        "displayValue": "April"
      },
      "percent": {
        "sortValue": 0.026,
        "displayValue": "2.6%"
      },
      "count": -32
    },
    {
      "alphabetical": "Hilo",
      "month": {
        "sortValue": 1,
        "displayValue": "January"
      },
      "percent": {
        "sortValue": -3.006,
        "displayValue": "-3.6%"
      },
      "count": {
        "sortValue": 0.002,
        "displayValue": "0.002"
      }
    },
    {
      "alphabetical": "Bravo",
      "month": {
        "sortValue": 12,
        "displayValue": "December"
      },
      "percent": {
        "sortValue": -0.036,
        "displayValue": "-300.6%"
      },
      "count": 0
    }
  ])
</script>

<style>
.table {
  width: 100%;
}
</style>