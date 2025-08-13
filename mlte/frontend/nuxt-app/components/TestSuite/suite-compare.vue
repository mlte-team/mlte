<template>
  <div>
    <h3>Header</h3>
    <b>{{ version1 }}</b>
    <HeaderDisplay :header="testSuite1.header" />
    <b>{{ version2 }}</b>
    <HeaderDisplay :header="testSuite2.header" />
    <div v-for="n in longestTestCaseList" :key="n">
      <h3>Test Case {{ n }}</h3>
      <b>{{ version1 }}</b>
      <div v-if="n - 1 < testSuite1.body.test_cases.length">
        <TestSuiteTestCaseDisplay
          :test-case="testSuite1.body.test_cases[n - 1]"
        />
      </div>
      <b>{{ version2 }}</b>
      <div v-if="n - 1 < testSuite2.body.test_cases.length">
        <TestSuiteTestCaseDisplay
          :test-case="testSuite2.body.test_cases[n - 1]"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  version1: {
    type: String,
    required: true,
  },
  version2: {
    type: String,
    required: true,
  },
  testSuite1: {
    type: Object,
    required: true,
    validator: (value: ArtifactModel<TestSuiteModel>) => {
      return value.body.artifact_type === "test_suite";
    },
  },
  testSuite2: {
    type: Object,
    required: true,
    validator: (value: ArtifactModel<TestSuiteModel>) => {
      return value.body.artifact_type === "test_suite";
    },
  },
});

const longestTestCaseList = computed(() =>
  Math.max(
    props.testSuite1.body.test_cases.length,
    props.testSuite2.body.test_cases.length,
  ),
);
</script>
