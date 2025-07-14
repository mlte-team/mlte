<template>
  <NuxtLayout name="base-layout">
    <title>Report</title>
    <template #page-title>Report</template>
    <UsaTextInput
      v-if="queryArtifactId === undefined"
      v-model="userInputArtifactId"
      :error="formErrors.identifier"
    >
      <template #label>
        Artifact ID
        <InfoIcon>
          The Artifact ID this report <br />
          will be saved under upon submission.
        </InfoIcon>
      </template>
      <template #error-message> Identifier cannot be empty </template>
    </UsaTextInput>

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

    <div style="text-align: right; margin-top: 1em">
      <UsaButton class="secondary-button" @click="cancelFormSubmission('/')">
        Cancel
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
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { cancelFormSubmission } from "~/composables/form-methods";

const config = useRuntimeConfig();
const token = useCookie("token");
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;
const forceSaveParam = queryArtifactId !== undefined;

const userInputArtifactId = ref("");
const form = ref<ReportModel>(new ReportModel());

const formErrors = ref({
  identifier: false,
});

if (queryArtifactId !== undefined) {
  form.value = await loadReportData(
    token.value as string,
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
}

async function submit() {
  const identifier = (queryArtifactId as string) || userInputArtifactId.value;
  if (identifier === "") {
    inputErrorAlert();
    return;
  }

  const artifact = {
    header: {
      identifier,
      type: "report",
      timestamp: -1,
      creator: "",
    },
    body: form.value,
  };

  if (isValidReport(artifact)) {
    try {
      await $fetch(
        config.public.apiPath +
          "/model/" +
          queryModel +
          "/version/" +
          queryVersion +
          "/artifact",
        {
          retry: 0,
          method: "POST",
          headers: {
            Authorization: "Bearer " + token.value,
          },
          body: {
            artifact,
            force: forceSaveParam,
            parents: false,
          },
          onRequestError() {
            requestErrorAlert();
          },
          onResponse({ response }) {
            if (response.ok) {
              successfulArtifactSubmission("report", identifier);
              if (useRoute().query.artifactId === undefined) {
                window.location.href =
                  "/report-form?" +
                  "model=" +
                  useRoute().query.model +
                  "&version=" +
                  useRoute().query.version +
                  "&artifactId=" +
                  identifier;
              }
            }
          },
          onResponseError({ response }) {
            handleHttpError(response.status, response._data.error_description);
          },
        },
      );
    } catch (exception) {
      console.log(exception);
    }
  } else {
    console.log("Invalid report.");
  }
}
</script>
