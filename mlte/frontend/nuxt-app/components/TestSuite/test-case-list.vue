<template>
  <div>
    <h2 class="section-header">Test Cases</h2>
    <span v-for="(testCase, caseIndex) in props.testCases" :key="caseIndex">
      <li>
        <b>Test Case: {{ caseIndex + 1 }}</b>
      </li>
      <TestSuiteTestCaseDisplay :test-case="testCase" />
    </span>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  testCases: {
    type: Object as PropType<Array<TestCaseModel>>,
    required: true,
  },
});
</script>
