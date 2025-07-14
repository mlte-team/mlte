<template>
  <table class="table usa-table usa-table--borderless">
    <thead>
      <tr>
        <th data-sortable scope="col" role="columnheader">Status</th>
        <th data-sortable scope="col" role="columnheader">
          Quality Attribute Scenario
        </th>
        <th data-sortable scope="col" role="columnheader">Measurement</th>
        <th data-sortable scope="col" role="columnheader">Test Case ID</th>
        <th data-sortable scope="col" role="columnheader">Message</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(result, key) in props.modelValue.results" :key="key">
        <td
          v-if="result.type == 'Success'"
          style="background-color: rgba(210, 232, 221, 255)"
        >
          {{ result.type }}
        </td>
        <td
          v-else-if="result.type == 'Info'"
          style="background-color: rgba(255, 243, 205, 255)"
        >
          {{ result.type }}
        </td>
        <td
          v-else-if="result.type == 'Failure'"
          style="background-color: rgba(248, 216, 219, 255)"
        >
          {{ result.type }}
        </td>
        <td v-else>{{ result.type }}</td>
        <td>
          <div
            v-for="(test_case, test_case_index) in props.modelValue.test_suite.test_cases"
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
