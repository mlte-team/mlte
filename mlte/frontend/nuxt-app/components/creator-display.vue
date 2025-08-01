<template>
  <div>
    <h3 style="display: inline">Last Modified by:</h3>
    {{ props.creator }} - {{ props.timestamp }}
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  creator: {
    type: String,
    required: false,
    default: "",
  },
  timestamp: {
    type: String,
    required: true,
  },
});
</script>
