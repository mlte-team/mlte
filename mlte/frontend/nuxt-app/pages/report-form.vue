<template>
  <NuxtLayout name="base-layout">
    <title>Report</title>
    <template #page-title>Report</template>
    <UsaTextInput
      v-if="queryArtifactId === undefined"
      v-model="userInputArtifactId"
    >
      <template #label>
        Artifact ID
        <InfoIcon>
          The Artifact ID this negotiation card <br />
          will be saved under upon submission.
        </InfoIcon>
      </template>
    </UsaTextInput>

    <FormFieldsSystemInformation v-model="form.nc_data.system" />

    <FormFieldsSystemRequirements v-model="form.nc_data.system_requirements" />

    <h2 class="section-header">Test Results (Quantitative Analysis)</h2>
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
        <tr v-for="(finding, index) in findings" :key="index">
          <td
            v-if="finding.status == 'Success'"
            style="background-color: rgba(210, 232, 221, 255)"
          >
            {{ finding.status }}
          </td>
          <td
            v-else-if="finding.status == 'Info'"
            style="background-color: rgba(255, 243, 205, 255)"
          >
            {{ finding.status }}
          </td>
          <td
            v-else-if="finding.status == 'Failure'"
            style="background-color: rgba(248, 216, 219, 255)"
          >
            {{ finding.status }}
          </td>
          <td v-else>{{ finding.status }}</td>
          <td>
            <div v-for="(item, qasIndex) in finding.qas_list" :key="qasIndex">
              {{ item.id }} - {{ item.qa }}
            </div>
          </td>
          <td>{{ finding.measurement }}</td>
          <td>{{ finding.test_case_id }}</td>
          <td>{{ finding.message }}</td>
        </tr>
      </tbody>
    </table>

    <!-- <h3>Comments</h3>
    <p>Free-form comments from model developers and system integrators.</p>
    <div v-for="(comment, commentIndex) in form.comments" :key="commentIndex">
      <UsaTextarea v-model="comment.content"> </UsaTextarea>
    </div> -->

    <!-- TODO: Implement this visualization -->
    <!-- <h3>Quantitative Analysis</h3>
    <p>No quantitative analysis included with this report.</p> -->

    <hr />
    <h1 class="section-header">Additional Context</h1>

    <FormFieldsDataFields v-model="form.nc_data.data" />

    <FormFieldsModelFields v-model="form.nc_data.model" />

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
const findings = ref<Array<Finding>>([]);
const form = ref<ReportModel>({
  artifact_type: "report",
  nc_data: {
    system: new SystemDescriptor(),
    data: [new DataDescriptor()],
    model: new ModelDescriptor(),
    system_requirements: [new QASDescriptor()],
  },
  test_results_id: "",
  comments: [{ content: "" }],
  quantitative_analysis: {},
});

if (useRoute().query.artifactId !== undefined) {
  const model = useRoute().query.model;
  const version = useRoute().query.version;
  const artifactId = useRoute().query.artifactId;

  const { data: reportData, error } = await useFetch<ReportApiResponse>(
    config.public.apiPath +
      "/model/" +
      model +
      "/version/" +
      version +
      "/artifact/" +
      artifactId,
    {
      retry: 0,
      method: "GET",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
  if (!error.value && reportData.value && isValidReport(reportData.value)) {
    form.value = reportData.value.body;
    if (reportData.value.body.test_results_id) {
      form.value.test_results_id = reportData.value.body.test_results_id;
      const testResultsRes = await fetchArtifact(
        token.value!,
        model as string,
        version as string,
        form.value.test_results_id,
      );

      // TODO : Consider error handling
      if (testResultsRes.body.artifact_type === "test_results") {
        findings.value = loadFindings(
          testResultsRes.body as TestResultsModel,
          form.value.nc_data.system_requirements,
        );
      }
    }
  }
}

async function submit() {
  const model = useRoute().query.model;
  const version = useRoute().query.version;
  const identifier =
    useRoute().query.artifactId?.toString() || userInputArtifactId.value;
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
          model +
          "/version/" +
          version +
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
