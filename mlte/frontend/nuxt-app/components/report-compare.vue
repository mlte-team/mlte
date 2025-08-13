<template>
  <h3>Header</h3>
  <b>{{ version1 }}</b>
  <HeaderDisplay :header="report1.header" />
  <b>{{ version2 }}</b>
  <HeaderDisplay :header="report2.header" />
  <h3>Test Results</h3>
  <div v-for="key in keySet" :key="key">
    <p><b>Result for: </b>{{ key }}</p>
    <b>Version: </b>{{ version1 }}
    <div v-if="key in report1.body.test_results.results">
      <TestSuiteResultView
        :result-key="key"
        :result="report1.body.test_results.results[key]"
        :test-cases="report1.body.test_suite.test_cases"
      />
    </div>
    <div v-else>No result</div>
    <b>Version: </b>{{ version2 }}
    <div v-if="key in report2.body.test_results.results">
      <TestSuiteResultView
        :result-key="key"
        :result="report2.body.test_results.results[key]"
        :test-cases="report2.body.test_suite.test_cases"
      />
    </div>
    <div v-else>No result</div>
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
  report1: {
    type: Object,
    required: true,
    validator: (value: ArtifactModel<ReportModel>) => {
      return value.body.artifact_type === "report";
    },
  },
  report2: {
    type: Object,
    required: true,
    validator: (value: ArtifactModel<ReportModel>) => {
      return value.body.artifact_type === "report";
    },
  },
});

const keySet = computed(() => {
  const combinedKeys = [
    ...Object.keys(props.report1.body.test_results.results),
    ...Object.keys(props.report2.body.test_results.results),
  ];
  const keySet = new Set(combinedKeys);
  return [...keySet];
});
</script>
