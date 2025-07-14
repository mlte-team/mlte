<template>
  <NuxtLayout name="base-layout">
    <title>Report</title>
    <template #page-title>Report</template>
    <h1 class="section-header">{{ queryArtifactId }}</h1>

    <FormFieldsSystemInformation v-model="form.negotiation_card.system" />

    <FormFieldsSystemRequirements
      v-model="form.negotiation_card.system_requirements"
    />

    <h2 class="section-header">Test Results</h2>
    <form-fields-results-table v-model="form.test_results" />

    <!-- <h3>Comments</h3>
    <p>Free-form comments from model developers and system integrators.</p>
    <div v-for="(comment, commentIndex) in form.comments" :key="commentIndex">
      <UsaTextarea v-model="comment.content"> </UsaTextarea>
    </div> -->

    <hr />
    <h1 class="section-header">Additional Context</h1>

    <FormFieldsDataFields v-model="form.negotiation_card.data" />

    <FormFieldsModelFields v-model="form.negotiation_card.model" />

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="cancelFormSubmission('/')">
        Back
      </UsaButton>
      <NuxtLink
        target="_blank"
        :to="{
          path: '/report-export',
          query: {
            model: queryModel,
            version: queryVersion,
            artifactId: queryArtifactId,
          },
        }"
      >
        <UsaButton class="primary-button"> Export </UsaButton>
      </NuxtLink>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { cancelFormSubmission } from "~/composables/form-methods";

const token = useCookie("token");
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;

const form = ref<ReportModel>(new ReportModel());

if (queryArtifactId !== undefined) {
  form.value = await loadReportData(
    token.value as string,
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
}
</script>
