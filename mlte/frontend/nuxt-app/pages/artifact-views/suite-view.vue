<template>
  <NuxtLayout name="base-layout">
    <title>Test Suite</title>
    <template #page-title>Test Suite</template>
    <h1 class="section-header">{{ queryArtifactId }}</h1>
    <CreatorDisplay :creator="creator" :timestamp="timestamp" />

    <div>
      <h2 class="section-header">Test Cases</h2>
      <ol>
        <li
          v-for="(testCase, caseIndex) in suiteBody.test_cases"
          :key="caseIndex"
        >
          {{ testCase.identifier }}
          <ul>
            <li><b>Goal: </b>{{ testCase.goal }}</li>
            <li>
              <b>Quality Attribute Scenario List</b>
              <ul>
                <li
                  v-for="(qas, qasIndex) in testCase.qas_list"
                  :key="qasIndex"
                >
                  {{ qas }}
                </li>
              </ul>
            </li>
            <li>
              <b>Measurement</b>
              <ul>
                <li>
                  <b>Measurement Class: </b
                  >{{ testCase.measurement.measurement_class }}
                </li>
                <li>
                  <b>Output Class: </b>{{ testCase.measurement.output_class }}
                </li>
                <li
                  v-if="
                    Object.keys(testCase.measurement.additional_data).length !==
                    0
                  "
                >
                  <b>Additional Data</b>
                  <ul>
                    <li
                      v-for="(value, key) in testCase.measurement
                        .additional_data"
                      :key="key"
                    >
                      {{ key }}: {{ value }}
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
            <li>
              <b>Validator</b>
              <ul>
                <li>
                  <b>Boolean Expression: </b
                  >{{ testCase.validator.bool_exp_str }}
                </li>
                <li>
                  <b>Thresholds</b>
                  <ul>
                    <li
                      v-for="(threshold, thresholdIndex) in testCase.validator
                        .thresholds"
                      :key="thresholdIndex"
                    >
                      {{ threshold }}
                    </li>
                  </ul>
                </li>
                <li><b>Success: </b>{{ testCase.validator.success }}</li>
                <li><b>Failure: </b>{{ testCase.validator.failure }}</li>
                <li><b>Info: </b>{{ testCase.validator.info }}</li>
                <li>
                  <b>Input Types</b>
                  <ul>
                    <li
                      v-for="(type, typeIndex) in testCase.validator
                        .input_types"
                      :key="typeIndex"
                    >
                      {{ type }}
                    </li>
                  </ul>
                </li>
                <li>
                  <b>Creator Entity: </b>{{ testCase.validator.creator_entity }}
                </li>
                <li>
                  <b>Creator Function: </b
                  >{{ testCase.validator.creator_function }}
                </li>
                <li>
                  <b>Creator Args</b>
                  <ul>
                    <li
                      v-for="(arg, argIndex) in testCase.validator.creator_args"
                      :key="argIndex"
                    >
                      {{ arg }}
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ol>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;

const creator = ref("");
const timestamp = ref("");
const suiteBody = ref<TestSuiteModel>(new TestSuiteModel());

if (queryArtifactId !== undefined) {
  const suite = await getSuite(
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
  if (suite) {
    creator.value = suite.header.creator;
    timestamp.value = timestampToString(suite.header.timestamp);
    suiteBody.value = suite.body;
  }
}
</script>
