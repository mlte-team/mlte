<template>
  <table class="table usa-table usa-table--borderless">
    <thead>
      <tr>
        <th scope="col" role="columnheader">Status</th>
        <th scope="col" role="columnheader">Quality Attribute Scenario</th>
        <th scope="col" role="columnheader">Measurement</th>
        <th scope="col" role="columnheader">Test Case ID</th>
        <th scope="col" role="columnheader">Message</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(result, key) in props.modelValue.results" :key="key">
        <td v-if="result.type == 'Success'" class="success-td">
          {{ result.type }}
        </td>
        <td v-else-if="result.type == 'Info'" class="info-td">
          {{ result.type }}
        </td>
        <td v-else-if="result.type == 'Failure'" class="failure-td">
          {{ result.type }}
        </td>
        <td v-else>{{ result.type }}</td>
        <td>
          <div
            v-for="(test_case, test_case_index) in props.modelValue.test_suite
              .test_cases"
            :key="test_case_index"
          >
            <span v-if="key == test_case.identifier">
              <span
                v-for="(qas, qasIndex) in test_case.qas_list"
                :key="qasIndex"
              >
                {{ qas }} - {{ key }}
              </span>
            </span>
          </div>
        </td>
        <td v-if="result.evidence_metadata">
          {{ result.evidence_metadata.measurement.measurement_class }}
        </td>
        <td v-else>Manually validated</td>
        <td v-if="result.evidence_metadata">
          {{ result.evidence_metadata.test_case_id }}
        </td>
        <td v-else>Manually validated</td>
        <td>{{ result.message }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  modelValue: {
    type: Object as PropType<TestResultsModel>,
    required: true,
  },
});
</script>
