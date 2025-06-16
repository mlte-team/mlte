<template>
  <div class="report-body">
    <div class="report-header rounded-border section-margin">
      <div class="header-img">
        <img src="~/assets/img/MLTE_Black.svg" height="75px" width="75px" />
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
        author details <br />
        author details <br />
        author details
      </div>
    </div>

    <div class="rounded-border section-margin">
      <h3 class="insection-margin">Overview</h3>
      <hr />
      <div
        v-for="(goal, goalIndex) in form.nc_data.system.goals"
        :key="goalIndex"
      >
        <div class="info-box-row insection-margin">
          <div class="info-box-third rounded-border">
            Goal {{ goalIndex + 1 }}:<br />
            {{ goal.description }}
          </div>
          <div class="info-box-two-third rounded-border">
            Metrics and Baselines: <br />
            <div
              v-for="(metric, metricIndex) in goal.metrics"
              :key="metricIndex"
            >
              {{ metricIndex + 1 }}. {{ metric.description }} -
              {{ metric.baseline }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="rounded-border insection-margin">
      <h3>Results</h3>
    </div>
    <table
      class="table usa-table usa-table--borderless section-margin"
      style="margin-top: 0px"
    >
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
        <tr v-for="finding in findings" :key="finding.test_case_id">
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
            <div v-for="(item, index) in finding.qas_list" :key="index">
              {{ item.id }} - {{ item.qa }}
            </div>
          </td>
          <td>{{ finding.measurement }}</td>
          <td>{{ finding.test_case_id }}</td>
          <td>{{ finding.message }}</td>
        </tr>
      </tbody>
    </table>

    <div class="rounded-border">
      <h3>System Information</h3>
      <hr />
      <div class="info-box-row insection-margin">
        <div class="info-box-third rounded-border">
          ML Problem Type: <br />
          {{ form.nc_data.system.problem_type }}
        </div>
        <div class="info-box-third rounded-border">
          ML Task: <br />
          {{ form.nc_data.system.task }}
        </div>
        <div class="info-box-third rounded-border">
          Usage Context: <br />
          {{ form.nc_data.system.usage_context }}
        </div>
      </div>

      <div class="info-box-row">
        <div class="info-box-third rounded-border">
          FP Risk: <br />
          {{ form.nc_data.system.risks.fp }}
        </div>
        <div class="info-box-third rounded-border">
          FN Risk: <br />
          {{ form.nc_data.system.risks.fn }}
        </div>
        <div class="info-box-third rounded-border">
          Other Risks: <br />
          {{ form.nc_data.system.risks.other }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const token = useCookie("token");

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

const model = useRoute().query.model;
const version = useRoute().query.version;
const artifactId = useRoute().query.artifactId;

form.value = await loadReportData(
  token.value as string,
  model as string,
  version as string,
  artifactId as string,
);

if (form.value.test_results_id) {
  findings.value = await loadTestResults(
    token.value as string,
    model as string,
    version as string,
    form.value.test_results_id,
    form.value.nc_data.system_requirements,
  );
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
  padding: 1ch 1ch 1ch 1ch;
}

.section-margin {
  margin-bottom: 3ch;
}

.insection-margin {
  margin-bottom: 2ch;
}

.report-header {
  display: flex;
  justify-content: space-evenly;
}

.header-img {
  width: 25ch;
}

.spacer {
  width: 25ch;
}

.header-title {
  text-align: center;
  width: 30ch;
}

.header-authors {
  width: 25ch;
  display: flex;
  align-items: center;
}

.info-box-row {
  display: flex;
  justify-content: space-evenly;
}

.info-box-third {
  width: 35ch;
}

.info-box-two-third {
  width: 70ch;
}
</style>
