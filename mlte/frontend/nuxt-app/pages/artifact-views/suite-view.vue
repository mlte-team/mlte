<template>
  <NuxtLayout name="base-layout">
    <title>Test Suite</title>
    <template #page-title>Test Suite</template>
    <h1 class="section-header">{{ queryArtifactId }}</h1>
    <CreatorDisplay :creator="creator" :timestamp="timestamp" />

    <TestSuiteTestCaseList :test-cases="suiteBody.test_cases" />
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;

const creator = ref("");
const timestamp = ref("");
const suiteBody = ref<TestSuiteModel>(new TestSuiteModel());

if (queryArtifactId !== undefined) {
  const suite = await getSuite(
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
  if (suite) {
    creator.value = suite.header.creator;
    timestamp.value = timestampToString(suite.header.timestamp);
    suiteBody.value = suite.body;
  }
}
</script>
