<template>
  <NuxtLayout name="base-layout">
    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">MLTE REPORT</h1>

    <UsaTextInput
      v-if="useRoute().query.artifactId === undefined"
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

    <h2 class="section-header">MLTE Evaluation</h2>
    <table class="table usa-table usa-table--borderless">
      <thead>
        <tr>
          <th data-sortable scope="col" role="columnheader">Status</th>
          <th data-sortable scope="col" role="columnheader">Property</th>
          <th data-sortable scope="col" role="columnheader">Measurement</th>
          <th data-sortable scope="col" role="columnheader">Evidence ID</th>
          <th data-sortable scope="col" role="columnheader">Message</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="finding in findings" :key="finding.evidence_id">
          <td
            v-if="finding.status == 'Success'"
            style="background-color: rgba(210, 232, 221, 255)"
          >
            {{ finding.status }}
          </td>
          <td
            v-else-if="finding.status == 'Ignore'"
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
          <td>{{ finding.property }}</td>
          <td>{{ finding.measurement }}</td>
          <td>{{ finding.evidence_id }}</td>
          <td>{{ finding.message }}</td>
        </tr>
      </tbody>
    </table>

    <h3>Comments</h3>
    <p>Free-form comments from model developers and system integrators.</p>
    <div v-for="(comment, commentIndex) in form.comments" :key="commentIndex">
      <UsaTextarea v-model="comment.content"> </UsaTextarea>
    </div>

    <!-- TODO: Implement this visualization -->
    <h3>Quantitative Analysis</h3>
    <p>No quantitative analysis included with this report.</p>

    <FormFieldsDataFields v-model="form.nc_data.data" />

    <FormFieldsModelFields v-model="form.nc_data.model" />

    <div style="text-align: right; margin-top: 1em">
      <UsaButton class="secondary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" disabled @click="exportReport()">
        Export
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/here",
    text: "Report",
  },
]);

const userInputArtifactId = ref("");
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);

const findings = ref(null);
const form = ref({
  artifact_type: "report",
  nc_data: {
    system: {
      goals: [
        {
          description: "",
          metrics: [
            {
              description: "",
              baseline: "",
            },
          ],
        },
      ],
      problem_type: "classification",
      task: "",
      usage_context: "",
      risks: {
        fp: "",
        fn: "",
        other: "",
      },
    },
    data: [
      {
        description: "",
        source: "",
        classification: "unclassified",
        access: "",
        labeling_method: "",
        labels: [
          {
            name: "",
            description: "",
            percentage: 0,
          },
        ],
        fields: [
          {
            name: "",
            description: "",
            type: "",
            expected_values: "",
            missing_values: "",
            special_values: "",
          },
        ],
        rights: "",
        policies: "",
      },
    ],
    model: {
      development_compute_resources: {
        gpu: "0",
        cpu: "0",
        memory: "0",
        storage: "0",
      },
      deployment_platform: "",
      capability_deployment_mechanism: "",
      input_specification: [
        {
          name: "",
          description: "",
          type: "",
          expected_values: "",
        },
      ],
      output_specification: [
        {
          name: "",
          description: "",
          type: "",
          expected_values: "",
        },
      ],
      production_compute_resources: {
        gpu: "0",
        cpu: "0",
        memory: "0",
        storage: "0",
      },
    },
    system_requirements: [
      {
        quality: "<System Quality>",
        stimulus: "<Stimulus>",
        source: "<Source>",
        environment: "<Environment>",
        response: "<Response>",
        measure: "<Response Measure>",
      },
    ],
  },
  validated_spec_id: "",
  comments: [{ content: "" }],
  quantitative_analysis: {},
});

const classificationOptions = useClassificationOptions();
const problemTypeOptions = useProblemTypeOptions();

if (useRoute().query.artifactId !== undefined) {
  const model = useRoute().query.model;
  const version = useRoute().query.version;
  const artifactId = useRoute().query.artifactId;

  await useFetch(
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
      async onResponse({ response }) {
        if (response.ok) {
          if (isValidReport(response._data)) {
            form.value = response._data.body;
            const problemType = response._data.body.nc_data.system.problem_type;
            if (
              problemTypeOptions.value.find((x) => x.value === problemType)?.value !==
              undefined
            ) {
              form.value.nc_data.system.problem_type = problemTypeOptions.value.find(
                (x) => x.value === problemType,
              )?.value;
            }

            // Setting .value for each classification item to work in the select
            response._data.body.nc_data.data.forEach((item) => {
              const classification = item.classification;
              if (
                classificationOptions.value.find((x) => x.value === classification)
                  ?.value !== undefined
              ) {
                item.classification = classificationOptions.value.find(
                  (x) => x.value === classification,
                )?.value;
              }
            });

            if (response._data.body.validated_spec_id) {
              form.value.validated_spec_id =
                response._data.body.validated_spec_id;
              const validatedSpec = await fetchArtifact(
                token.value,
                model,
                version,
                form.value.validated_spec_id,
              );
              findings.value = loadFindings(validatedSpec);
            }
          }
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
}

async function submit() {
  const model = useRoute().query.model;
  const version = useRoute().query.version;

  let identifier = "";
  if (useRoute().query.artifactId === undefined) {
    identifier = userInputArtifactId.value;
  } else {
    identifier = useRoute().query.artifactId?.toString();
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
            force: forceSaveParam.value,
            parents: false,
          },
          onRequestError() {
            requestErrorAlert();
          },
          onResponseError({ response }) {
            if (response.status === 409) {
              conflictErrorAlert();
            } else {
              handleHttpError(
                response.status,
                response._data.error_description,
              );
            }
          },
        },
      );
      successfulArtifactSubmission("report", identifier);
      forceSaveParam.value = true;
    } catch {}
  } else {
    console.log("Invalid report.");
  }
}

// Export the current report.
function exportReport() {
  alert("Report export is not currently implemented.");
}
</script>
