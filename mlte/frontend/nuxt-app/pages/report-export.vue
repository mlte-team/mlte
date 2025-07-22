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
    <form-fields-results-table
      v-model="form.test_results"
      class="section-margin"
    />

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
const form = ref<ReportModel>(new ReportModel());

const model = useRoute().query.model;
const version = useRoute().query.version;
const artifactId = useRoute().query.artifactId;

form.value = await getReport(
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
