<template>
  <ul>
    <li>
      <b>Identifier: {{ header.identifier }}</b>
    </li>
    <li><b>Timestamp: </b>{{ timestampToString(header.timestamp) }}</li>
    <li><b>Creator: </b>{{ header.creator }}</li>
  </ul>
</template>

<script setup lang="ts">
import type { PropType } from "vue";
import { timestampToString } from "~/composables/util";

const props = defineProps({
  header: {
    type: Object as PropType<ArtifactHeader>,
    required: true,
  },
});
</script>
