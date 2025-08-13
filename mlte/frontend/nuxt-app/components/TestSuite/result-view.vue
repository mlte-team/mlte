<template>
  <div>
    <ul>
      <li><b>Status: </b>{{ result.type }}</li>
      <li>
        <b>Measurement: </b>
        <span v-if="result.evidence_metadata"
          >{{ result.evidence_metadata.measurement.measurement_class }}
        </span>
        <span v-else>None</span>
      </li>
      <li><b>Message: </b> {{ result.message }}</li>
      <li>
        <b>Quality Attribute Scenario</b>
        <ul>
          <span
            v-for="(test_case, test_case_index) in props.testCases"
            :key="test_case_index"
          >
            <li v-if="resultKey == test_case.identifier">
              <span
                v-for="(qas, qasIndex) in test_case.qas_list"
                :key="qasIndex"
              >
                {{ qas }} - {{ resultKey }}
              </span>
            </li>
          </span>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  resultKey: {
    type: String,
    required: true,
  },
  result: {
    type: Object as PropType<Result>,
    required: true,
  },
  testCases: {
    type: Object as PropType<Array<TestCaseModel>>,
    required: true,
  },
});
</script>
