<template>
  <div>
    <h2 class="section-header">Test Cases</h2>
    <ul>
      <li v-for="(testCase, caseIndex) in props.testCases" :key="caseIndex">
        <TestSuiteTestCaseDisplay :test-case="testCase" />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { TestSuiteTestCaseDisplay } from "#components";
import type { PropType } from "vue";

const props = defineProps({
  testCases: {
    type: Object as PropType<Array<TestCaseModel>>,
    required: true,
  },
});
</script>
