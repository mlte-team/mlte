<template>
  <div class="report-body">
    <div class="report-header rounded-border">
      <div class="header-img">
        <img
          src="~/assets/img/MLTE_Black.svg"
          height="75px"
          width="75px"
          />
      </div>

      <div class="spacer"></div>

      <div class="header-title centered-container">
        <h3>
          MLTE REPORT <br />
          {{ model }} Model 
        </h3>
      </div>

      <div class="spacer"></div>

      <div class="header-authors">
        author 1 <br />
        author 2 <br />
        author 3
      </div>      
    </div>

    <div class="rounded-border">
      <h3>Overview</h3>
    </div>

    <div class="rounded-border">
      <h3>Results</h3>
    </div>
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

    <div class="rounded-border">
      <h3>System Information</h3>
    </div>
    <div class="info-box-row">
      <div class="info-box rounded-border">
        ML Problem Type <br />
        {{ page_data.summary.problem_type }}
      </div>
      <div class="info-box rounded-border">
        ML Task <br />
        {{ page_data.summary.task }}
      </div>
      <div class="info-box rounded-border">
        Usage Context <br />
        {{ page_data.intended_use.usage_context }}
      </div>
    </div>

    <div class="info-box-row">
      <div class="info-box rounded-border">
        FP Risk <br />
        {{ page_data.risks.fp }}
      </div>
      <div class="info-box rounded-border">
        FN Risk <br />
        {{ page_data.risks.fn }}
      </div>
      <div class="info-box rounded-border">
        Other Risks <br />
        {{ page_data.risks.other }}
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const findings = ref(null);
const page_data = ref(null);

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
      if (isValidReport(response._data)) {
        page_data.value = response._data.body;

        if (response._data.body.performance.validated_spec_id) {
          page_data.value.performance.validated_spec_id =
            response._data.body.performance.validated_spec_id;
          const validatedSpec = await fetchArtifact(
            token.value,
            model,
            version,
            page_data.value.performance.validated_spec_id,
          );
          findings.value = loadFindings(validatedSpec);
        }
      }
    },
    onResponseError() {
      responseErrorAlert();
    },
  },
);

// Load findings from a validated specication.
function loadFindings(proxyObject: any) {
  console.log("loading findings");
  const findings = [];
  // TODO(Kyle): Standardize conversion of proxy objects.
  const validatedSpec = JSON.parse(JSON.stringify(proxyObject));
  validatedSpec.body.spec.properties.forEach((property) => {
    // TODO(Kyle): This is not portable to some browsers.
    const results = new Map(
      Object.entries(validatedSpec.body.results[property.name]),
    );
    results.forEach((value) => {
      const finding = {
        status: value.type,
        property: property.name,
        measurement: value.metadata.measurement_type,
        evidence_id: value.metadata.identifier.name,
        message: value.message,
      };
      findings.push(finding);
    });
  });
  return findings;
}
</script>

<style>
.report-body {
  width: 100%;
  max-width: 128ch;
}

.rounded-border {
  border: 1px solid black;
  border-radius: 15px;
}

.report-header {
  display: flex;
  justify-content: space-evenly;
}

.header-img {
  width: 25ch;
  border: 1px solid purple;
}

.spacer {
  width: 25ch;
  border: 1px solid orange;
}

.header-title {
  border: 1px solid red;
  text-align: center;
  width: 30ch;
}

.header-authors {
  width: 25ch;
  display: flex;
  align-items: center;
  
  border: 1px solid purple;
}

.info-box-row {
  display: flex;
  justify-content: space-evenly;
}

.info-box {
  width: 35ch;
}
</style>