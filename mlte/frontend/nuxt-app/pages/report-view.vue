<template>
  <NuxtLayout name="base-layout">
    <title>Report</title>
    <template #page-title>Report</template>
    <h1 class="section-header">{{ queryArtifactId }}</h1>

    <div>
      <h2 class="section-header">System Information</h2>
      <div>
        <b>Usage Context for the Model: </b>
        {{ report.negotiation_card.system.usage_context }}
      </div>

      <div>
        <b>Goals:</b>
        <ol>
          <li
            v-for="(goal, goalIndex) in report.negotiation_card.system.goals"
            :key="goalIndex"
          >
            <b>Goal {{ goalIndex + 1 }}</b>
            <ul>
              <li><b>Goal Description: </b>{{ goal.description }}</li>
              <li>
                <b>Metrics</b>
                <ol>
                  <li
                    v-for="(metric, metricIndex) in goal.metrics"
                    :key="metricIndex"
                  >
                    <b>Metric {{ metricIndex + 1 }}</b>
                    <ul>
                      <li><b>Description: </b>{{ metric.description }}</li>
                      <li><b>Baseline Source: </b>{{ metric.baseline }}</li>
                    </ul>
                  </li>
                </ol>
              </li>
            </ul>
          </li>
        </ol>
      </div>

      <div>
        <b>ML Problem Type: </b>
        {{ report.negotiation_card.system.problem_type }}
      </div>

      <div>
        <b>ML Task: </b>
        {{ report.negotiation_card.system.task }}
      </div>

      <div>
        <b>False Positive Risk: </b>
        {{ report.negotiation_card.system.risks.fp }}
      </div>

      <div>
        <b>False Negative Risk: </b>
        {{ report.negotiation_card.system.risks.fn }}
      </div>

      <div>
        <b>Other Risks of Producing Incorrect Results</b>
        <ol>
          <li
            v-for="(risk, riskIndex) in report.negotiation_card.system.risks
              .other"
            :key="riskIndex"
          >
            {{ risk }}
          </li>
        </ol>
      </div>
    </div>

    <div>
      <h2 class="section-header">System Requirements</h2>
      <ol>
        <li
          v-for="(requirement, requirementIndex) in report.negotiation_card
            .system_requirements"
          :key="requirementIndex"
        >
          {{ requirement.quality }}
          <ul>
            <li>{{ requirement.identifier }}</li>
            <li>
              {{ requirement.stimulus }} from {{ requirement.source }} during
              {{ requirement.environment }}. {{ requirement.response }}
              {{ requirement.measure }}.
            </li>
          </ul>
        </li>
      </ol>
    </div>

    <h2 class="section-header">Test Results</h2>
    <form-fields-results-table v-model="report.test_results" />

    <hr />
    <h1 class="section-header">Additional Context</h1>

    <div>
      <ol>
        <li
          v-for="(dataItem, datasetIndex) in report.negotiation_card.data"
          :key="datasetIndex"
        >
          <b>Description: </b>{{ dataItem.description }}
          <ul>
            <li><b>Source: </b> {{ dataItem.source }}</li>
            <li><b>Data Classification: </b> {{ dataItem.classification }}</li>
            <li>
              <b>Requirements and Constraints for Data Access: </b>
              {{ dataItem.access }}
            </li>
            <li>
              <b>Labels and Distribution: </b>
              <ul>
                <li><b>Labelling Method: </b>{{ dataItem.labeling_method }}</li>
                <li
                  v-for="(label, labelIndex) in dataItem.labels"
                  :key="labelIndex"
                >
                  <b>Label {{ labelIndex + 1 }}</b>
                  <ol>
                    <li><b>Label Name: </b>{{ label.name }}</li>
                    <li><b>Label Description: </b>{{ label.description }}</li>
                    <li><b>Percentage: </b>{{ label.percentage }}</li>
                  </ol>
                </li>
              </ul>
            </li>
            <li>
              <b>Data Schema</b>
              <ol>
                <li
                  v-for="(field, fieldIndex) in dataItem.fields"
                  :key="fieldIndex"
                >
                  <b>Data Schema {{ fieldIndex + 1 }}</b>
                  <ul>
                    <li><b>Field Name: </b> {{ field.name }}</li>
                    <li><b>Field Description: </b> {{ field.description }}</li>
                    <li><b>Field Type: </b> {{ field.type }}</li>
                    <li>
                      <b>Expected Values: </b> {{ field.expected_values }}
                    </li>
                    <li>
                      <b>Handling Missing Values: </b>
                      {{ field.missing_values }}
                    </li>
                    <li>
                      <b>Handling Special Values: </b>
                      {{ field.special_values }}
                    </li>
                  </ul>
                </li>
              </ol>
            </li>
            <li><b>Data Rights: </b>{{ dataItem.rights }}</li>
            <li><b>Data Policies: </b>{{ dataItem.policies }}</li>
          </ul>
        </li>
      </ol>
    </div>

    <div>
      <h2 class="section-header">Model Information</h2>
      <div>
        <b>Development Compute Resources</b>
        <ul>
          <li>
            <b>Graphics Processing Units (GPUs): </b
            >{{
              report.negotiation_card.model.development_compute_resources.gpu
            }}
          </li>
          <li>
            <b>Central Processing Units (CPUs): </b
            >{{
              report.negotiation_card.model.development_compute_resources.cpu
            }}
          </li>
          <li>
            <b>Memory: </b
            >{{
              report.negotiation_card.model.development_compute_resources.memory
            }}
          </li>
          <li>
            <b>Storage: </b
            >{{
              report.negotiation_card.model.development_compute_resources
                .storage
            }}
          </li>
        </ul>
      </div>

      <div>
        <b>Deployment Platform: </b>
        {{ report.negotiation_card.model.deployment_platform }}
      </div>

      <div>
        <b>Capability Deployment Mechanism: </b>
        {{ report.negotiation_card.model.capability_deployment_mechanism }}
      </div>

      <div>
        <b>Input Specification</b>
        <ol>
          <li
            v-for="(inputSpec, inputSpecIndex) in report.negotiation_card.model
              .input_specification"
            :key="inputSpecIndex"
          >
            <b>Input {{ inputSpecIndex + 1 }}</b>
            <ul>
              <li><b>Input Name: </b>{{ inputSpec.name }}</li>
              <li><b>Description: </b>{{ inputSpec.description }}</li>
              <li><b>Type: </b>{{ inputSpec.type }}</li>
              <li><b>Expected Values: </b>{{ inputSpec.expected_values }}</li>
            </ul>
          </li>
        </ol>
      </div>

      <div>
        <b>Output Specification</b>
        <ol>
          <li
            v-for="(outputSpec, outputSpecIndex) in report.negotiation_card
              .model.output_specification"
            :key="outputSpecIndex"
          >
            <b>Output {{ outputSpecIndex + 1 }}</b>
            <ul>
              <li><b>Output Name: </b>{{ outputSpec.name }}</li>
              <li><b>Description: </b>{{ outputSpec.description }}</li>
              <li><b>Type: </b>{{ outputSpec.type }}</li>
              <li><b>Expected Values: </b>{{ outputSpec.expected_values }}</li>
            </ul>
          </li>
        </ol>
      </div>

      <div>
        <b>Production Compute Resources</b>
        <ul>
          <li>
            <b>Graphics Processing Units (GPUs): </b
            >{{
              report.negotiation_card.model.production_compute_resources.gpu
            }}
          </li>
          <li>
            <b>Central Processing Units (CPUs): </b
            >{{
              report.negotiation_card.model.production_compute_resources.cpu
            }}
          </li>
          <li>
            <b>Memory: </b
            >{{
              report.negotiation_card.model.production_compute_resources.memory
            }}
          </li>
          <li>
            <b>Storage: </b
            >{{
              report.negotiation_card.model.production_compute_resources.storage
            }}
          </li>
        </ul>
      </div>
    </div>

    <div class="submit-footer">
      <NuxtLink
        :to="{
          path: '/',
        }"
      >
        <UsaButton class="primary-button"> Back </UsaButton>
      </NuxtLink>
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
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;

const report = ref<ReportModel>(new ReportModel());

if (queryArtifactId !== undefined) {
  report.value = await getReport(
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
}
</script>
