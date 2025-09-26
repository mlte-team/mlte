<template>
  <NuxtLayout name="base-layout">
    <title>Evidence</title>
    <template #page-title>Evidence</template>
    <h1 class="section-header">{{ queryArtifactId }}</h1>
    <CreatorDisplay :creator="creator" :timestamp="timestamp" />

    <div>
      <h2 class="section-header">Evidence</h2>
      <EvidenceMetadataDisplay :evidence-metadata="evidenceBody.metadata" />

      <div><b>Evidence Class: </b> {{ evidenceBody.evidence_class }}</div>

      <div>
        <b>Value: </b>
        <ul>
          <li><b>Type: </b>{{ evidenceBody.value.evidence_type }}</li>
          <span v-if="evidenceBody.value.evidence_type === 'integer'">
            <li><b>Integer: </b>{{ evidenceBody.value.integer }}</li>
            <li><b>unit: </b>{{ evidenceBody.value.unit }}</li>
          </span>
          <span v-else-if="evidenceBody.value.evidence_type === 'real'">
            <li><b>Real: </b>{{ evidenceBody.value.real }}</li>
            <li><b>Unit: </b>{{ evidenceBody.value.unit }}</li>
          </span>
          <span v-else-if="evidenceBody.value.evidence_type === 'opaque'">
            <li>
              <b>Data: </b>
              <ul>
                <li v-for="(value, key) in evidenceBody.value.data" :key="key">
                  {{ key }} - {{ value }}
                </li>
              </ul>
            </li>
          </span>
          <span v-else-if="evidenceBody.value.evidence_type === 'image'">
            <!-- TODO: Can this show the image? -->
            <li><b>Data: </b>{{ evidenceBody.value.data }}</li>
          </span>
          <span v-else-if="evidenceBody.value.evidence_type === 'array'">
            <li>
              <b>Data: </b>
              <ul>
                <li
                  v-for="(item, index) in evidenceBody.value.data"
                  :key="index"
                >
                  {{ item }}
                </li>
              </ul>
            </li>
          </span>
          <span v-else-if="evidenceBody.value.evidence_type === 'string'">
            <li><b>String: </b>{{ evidenceBody.value.string }}</li>
          </span>
        </ul>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;

const creator = ref("");
const timestamp = ref("");
const evidenceBody = ref<EvidenceModel>(new EvidenceModel());

if (queryArtifactId !== undefined) {
  const evidence = await getEvidence(
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
  if (evidence) {
    creator.value = evidence.header.creator;
    timestamp.value = timestampToString(evidence.header.timestamp);
    evidenceBody.value = evidence.body;
  }
}
</script>
