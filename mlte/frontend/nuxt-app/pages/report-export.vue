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
        v-for="(goal, goalIndex) in form.negotiation_card.system.goals"
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
        <tr v-for="(result, key) in form.test_results.results" :key="key">
          <td
            v-if="result.type == 'Success'"
            style="background-color: rgba(210, 232, 221, 255)"
          >
            {{ result.type }}
          </td>
          <td
            v-else-if="result.type == 'Info'"
            style="background-color: rgba(255, 243, 205, 255)"
          >
            {{ result.type }}
          </td>
          <td
            v-else-if="result.type == 'Failure'"
            style="background-color: rgba(248, 216, 219, 255)"
          >
            {{ result.type }}
          </td>
          <td v-else>{{ result.type }}</td>
          <td>
            <div
              v-for="(test_case, test_case_index) in form.test_results
                .test_suite.test_cases"
              :key="test_case_index"
            >
              <span v-if="key == test_case.identifier">
                <span
                  v-for="(qas, qasIndex) in test_case.qas_list"
                  :key="qasIndex"
                >
                  {{ qas }} - {{ key }}
                </span>
              </span>
            </div>
          </td>
          <td v-if="result.evidence_metadata">
            {{ result.evidence_metadata.measurement.measurement_class }}
          </td>
          <td v-else>Manually validated</td>
          <td v-if="result.evidence_metadata">
            {{ result.evidence_metadata.test_case_id }}
          </td>
          <td v-else>Manually validated</td>
          <td>{{ result.message }}</td>
        </tr>
      </tbody>
    </table>

    <div class="rounded-border">
      <h3>System Information</h3>
      <hr />
      <div class="info-box-row insection-margin">
        <div class="info-box-third rounded-border">
          ML Problem Type: <br />
          {{ form.negotiation_card.system.problem_type }}
        </div>
        <div class="info-box-third rounded-border">
          ML Task: <br />
          {{ form.negotiation_card.system.task }}
        </div>
        <div class="info-box-third rounded-border">
          Usage Context: <br />
          {{ form.negotiation_card.system.usage_context }}
        </div>
      </div>

      <div class="info-box-row">
        <div class="info-box-third rounded-border">
          FP Risk: <br />
          {{ form.negotiation_card.system.risks.fp }}
        </div>
        <div class="info-box-third rounded-border">
          FN Risk: <br />
          {{ form.negotiation_card.system.risks.fn }}
        </div>
        <div class="info-box-third rounded-border">
          Other Risks: <br /><br />
          <div
            v-for="(risk, riskIndex) in form.negotiation_card.system.risks
              .other"
            :key="riskIndex"
          >
            <div class="info-box-row insection-margin">
              <div class="info-box-third rounded-border">
                Risk {{ riskIndex + 1 }}:<br />
                {{ risk }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const token = useCookie("token");

const form = ref<ReportModel>(new ReportModel());

const model = useRoute().query.model;
const version = useRoute().query.version;
const artifactId = useRoute().query.artifactId;

form.value = await loadReportData(
  token.value as string,
  model as string,
  version as string,
  artifactId as string,
);
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
