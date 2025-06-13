<template>
  <h2 class="section-header">System Information</h2>
  <UsaTextarea
    v-model="props.modelValue.usage_context"
    style="margin-bottom: 1em"
  >
    <template #label>
      Usage Context for the Model
      <InfoIcon>
        Who is intended to utilize the system/model; how the results of the
        model are <br />
        going to be used by end users or in the context of a larger system.
        <br />
        <br />
        <i
          >Example: Model results are consumed by a system component that shows
          <br />
          an intel analyst a list of matching voice recordings.</i
        >
      </InfoIcon>
    </template>
  </UsaTextarea>

  <div class="input-group">
    <SubHeader :render-example="false">
      Goals
      <template #info>
        Goals or objectives that the model is going to help satisfy as part of
        the system.
      </template>
    </SubHeader>
    <div v-for="(goal, goalIndex) in props.modelValue.goals" :key="goalIndex">
      <h3 class="no-margin-sub-header">Goal {{ goalIndex + 1 }}</h3>
      <UsaTextInput v-model="goal.description">
        <template #label>
          Goal Description
          <InfoIcon>
            Short description for the goal.
            <br />
            <br />
            <i
              >Example: Identify voice recordings that belong to a given person
              of interest.</i
            >
          </InfoIcon>
        </template>
      </UsaTextInput>

      <SubHeader :render-example="false" :render-info="false">
        Metrics
      </SubHeader>
      <div v-for="(metric, metricIndex) in goal.metrics" :key="metricIndex">
        <div class="inline-input-left">
          <UsaTextInput v-model="metric.description">
            <template #label>
              Description
              <InfoIcon>
                Performance metric that captures the system's ability to
                accomplish the goal,<br />
                i.e., acceptance criteria for determining that the model is
                performing correctly.
                <br />
                <br />
                <i>Example: Accuracy > 90%</i>
              </InfoIcon>
            </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="metric.baseline">
            <template #label>
              Baseline Source
              <InfoIcon>
                Indicates where the performance metric goal comes from, or why
                it is <br />
                believed to be achievable.
                <br />
                <br />
                <i
                  >Example: Human accuracy for matching voices is ~60% as stated
                  in the paper<br />
                  by Smith et al.</i
                ><br />
              </InfoIcon>
            </template>
          </UsaTextInput>
        </div>
        <div class="inline-button">
          <DeleteButton @click="deleteMetric(goalIndex, metricIndex)">
            Delete Metric
          </DeleteButton>
        </div>
      </div>
      <AddButton class="margin-button" @click="addMetric(goalIndex)">
        Add Metric
      </AddButton>
      <div class="inline-button" style="vertical-align: bottom">
        <DeleteButton @click="deleteGoal(goalIndex)">
          Delete Goal
        </DeleteButton>
      </div>
      <hr />
    </div>

    <AddButton class="margin-button" @click="addGoal()"> Add Goal </AddButton>
  </div>

  <UsaSelect
    v-model="props.modelValue.problem_type"
    :options="problemTypeOptions"
  >
    <template #label>
      ML Problem Type
      <InfoIcon>
        Type of ML problem that the model is intended to solve.
        <br />
        <br />
        <i
          >Example: Classification, Clustering, Detection, and others in
          drop-down list.</i
        >
      </InfoIcon>
    </template>
  </UsaSelect>

  <UsaTextInput v-model="props.modelValue.task">
    <template #label>
      ML Task
      <InfoIcon>
        Well-defined task that model is expected to perform, or problem that the
        model is expected to solve.
        <br />
        <br />
        <i>Example: Match voice recordings spoken by the same person.</i>
      </InfoIcon>
    </template>
  </UsaTextInput>

  <UsaTextInput v-model="props.modelValue.risks.fp">
    <template #label>
      False Positive Risk
      <InfoIcon>
        What is the risk of producing a false positive?
        <br />
        <br />
        <i
          >Example: Incorrect positive results will cause extra work for the
          <br />
          intel analyst that needs to analyze every recording flagged by the
          model.</i
        >
      </InfoIcon>
    </template>
  </UsaTextInput>

  <UsaTextInput v-model="props.modelValue.risks.fn">
    <template #label>
      False Negative Risk
      <InfoIcon>
        What is the risk of producing a false negative?
        <br />
        <br />
        <i
          >Example: Incorrect negative results means that the model will
          <br />
          not flag suspicious recordings, which means that intel analysts
          <br />
          might miss information that is crucial to an investigation.</i
        >
      </InfoIcon>
    </template>
  </UsaTextInput>

  <UsaTextInput v-model="props.modelValue.risks.other">
    <template #label>
      Other Risks of Producing Incorrect Results
      <InfoIcon>
        What are other risks of producing incorrect results?
      </InfoIcon>
    </template>
  </UsaTextInput>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  modelValue: {
    type: Object as PropType<SystemDescriptor>,
    required: true,
  },
});

const problemTypeOptions = useProblemTypeOptions();

const parentAddGoal = () => {
  addGoal();
};

defineExpose({
  parentAddGoal,
});

function addGoal() {
  props.modelValue.goals.push(new GoalDescriptor());
}

function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    props.modelValue.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex: number) {
  props.modelValue.goals[goalIndex].metrics.push(new MetricDescriptor());
}

function deleteMetric(goalIndex: number, metricIndex: number) {
  if (confirm("Are you sure you want to delete this metric?")) {
    props.modelValue.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}
</script>
