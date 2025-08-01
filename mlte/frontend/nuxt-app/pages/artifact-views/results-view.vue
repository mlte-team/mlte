<template>
  <NuxtLayout name="base-layout">
    <title>Test Results</title>
    <template #page-title>Test Results</template>
    <h1 class="section-header">{{ queryArtifactId }}</h1>
    <CreatorDisplay :creator="creator" :timestamp="timestamp" />

    <div>
      <h2 class="section-header">Results</h2>
      <ul>
        <li v-for="(value, key) in resultsBody.results" :key="key">
          {{ key }}
          <ul>
            <li><b>Type: </b>{{ value.type }}</li>
            <li v-if="value.evidence_metadata">
              <EvidenceMetadataDisplay
                :evidence-metadata="value.evidence_metadata"
              />
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <TestCaseDisplay :test-cases="resultsBody.test_suite.test_cases" />
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;

const creator = ref("");
const timestamp = ref("");
const resultsBody = ref<TestResultsModel>(new TestResultsModel());

if (queryArtifactId !== undefined) {
  const results = await getResults(
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
  if (results) {
    creator.value = results.header.creator;
    timestamp.value = timestampToString(results.header.timestamp);
    resultsBody.value = results.body;
  }
}
</script>
