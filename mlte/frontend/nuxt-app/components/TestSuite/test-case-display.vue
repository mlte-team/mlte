<template>
  <div>
    <ul>
      <li><b>Goal: </b>{{ testCase.goal }}</li>
      <li>
        <b>Quality Attribute Scenario List</b>
        <ul>
          <li v-for="(qas, qasIndex) in testCase.qas_list" :key="qasIndex">
            {{ qas }}
          </li>
        </ul>
      </li>
      <li>
        <MeasurementDataDisplay :measurement="testCase.measurement" />
      </li>
      <li>
        <b>Validator</b>
        <ul>
          <li>
            <b>Boolean Expression: </b>{{ testCase.validator.bool_exp_str }}
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
                v-for="(type, typeIndex) in testCase.validator.input_types"
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
            <b>Creator Function: </b>{{ testCase.validator.creator_function }}
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
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  testCase: {
    type: Object as PropType<TestCaseModel>,
    required: true,
  },
});
</script>
