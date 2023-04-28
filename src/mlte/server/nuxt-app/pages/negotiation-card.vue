<template>
  <div style="padding: 50px">
    <UsaBreadcrumb
      :items="path"
    />
  </div>
</template>

<script setup>
  var path = ref([
    {
      "to": "/",
      "text": "Artifact Store"
    },
    {
      "to": "/negotiation-store",
      "text": "Negotiation Card"
    }
  ])
</script>