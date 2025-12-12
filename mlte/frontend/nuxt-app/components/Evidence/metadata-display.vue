<template>
  <div>
    <b>Evidence Metadata:</b>
    <ul>
      <li><b>Test Case ID: </b>{{ props.evidenceMetadata.test_case_id }}</li>
      <li>
        <MeasurementDataDisplay
          :measurement="props.evidenceMetadata.measurement"
        />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  evidenceMetadata: {
    type: Object as PropType<EvidenceMetadata>,
    required: true,
  },
});
</script>
