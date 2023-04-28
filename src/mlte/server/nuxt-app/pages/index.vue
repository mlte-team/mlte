<template>
  <div style='margin:50px'>
    <UsaTable
      :headers="head"
      :rows="rows"
    >
    </UsaTable>
  </div>
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
      "sortable": false
    },
    {
      "id": "percent",
      "label": "Percent",
      "sortable": false
    },
    {
      "id": "count",
      "label": "Count",
      "sortable": false
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