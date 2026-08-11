<template>
  <div>
    <h3 style="display: inline">Model:</h3>
    {{ props.model }}
    <h3 style="display: inline">Version:</h3>
    {{ props.version }}
    <h3 style="display: inline">ID:</h3>
    {{ props.id }}
  </div>
  <div>
    <h3 style="display: inline">Last Modified by:</h3>
    {{ props.creator }} - {{ props.timestamp }}
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    id: string;
    model: string;
    version: string;
    creator: string;
    timestamp: string;
  }>(),
  {
    id: "",
    model: "",
    version: "",
    creator: "",
  },
);
</script>
