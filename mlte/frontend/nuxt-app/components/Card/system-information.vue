<template>
  <CollapsibleHeader v-model="displaySection" @change="displaySection = $event">
    <template #title> System Context for Model </template>
  </CollapsibleHeader>

  <div v-if="displaySection">
    <div class="input-group">
      <SubHeader :render-example="false">
        General Information
        <template #info>
          General information about the problem and usage context.
        </template>
      </SubHeader>
      <UsaTextarea v-model="props.modelValue.task" style="height: 5.5rem">
        <template #label>
          ML Task
          <InfoIcon>
            Well-defined task that model is expected to perform, or problem that
            the model is expected to solve.
            <br />
            <br />
            <i>Example: Match voice recordings spoken by the same person.</i>
          </InfoIcon>
        </template>
      </UsaTextarea>

      <CustomListProblemTypeSelect v-model="props.modelValue.problem_type" />

      <UsaTextarea
        v-model="props.modelValue.usage_context"
        style="height: 5.5rem"
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
              >Example: Model results are consumed by a system component that
              shows
              <br />
              an intel analyst a list of matching voice recordings.</i
            >
          </InfoIcon>
        </template>
      </UsaTextarea>
    </div>

    <div class="input-group">
      <SubHeader :render-example="false">
        Goals
        <template #info>
          Goals or objectives that the model is going to help satisfy as part of
          the system.
        </template>
      </SubHeader>

      <hr />

      <div v-for="(goal, goalIndex) in props.modelValue.goals" :key="goalIndex">
        <h3 class="no-margin-sub-header">Goal {{ goalIndex + 1 }}</h3>
        <UsaTextarea v-model="goal.description" style="height: 5.5rem">
          <template #label>
            Goal Description
            <InfoIcon>
              Short description for the goal.
              <br />
              <br />
              <i
                >Example: Identify voice recordings that belong to a given
                person of interest.</i
              >
            </InfoIcon>
          </template>
        </UsaTextarea>

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
                    >Example: Human accuracy for matching voices is ~60% as
                    stated in the paper<br />
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

    <div class="input-group">
      <SubHeader :render-example="false">
        Risks
        <template #info>
          Risks to model performance such as false positives, false negatives,
          hallucinations, or bias.
        </template>
      </SubHeader>

      <hr />

      <div v-for="(risk, riskIndex) in props.modelValue.risks" :key="riskIndex">
        <h3 class="no-margin-sub-header">Risk {{ riskIndex + 1 }}</h3>
        <UsaTextarea
          v-model="props.modelValue.risks[riskIndex]"
          style="height: 5.5rem"
        >
          <template #label>
            Risk
            <InfoIcon>
              Short description for the risk.
              <br />
              <br />
              <i>
                Example: Model may not indicate proper results if data is out
                bounds.
              </i>
            </InfoIcon>
          </template>
        </UsaTextarea>

        <div class="margin-button">
          <DeleteButton @click="deleteRisk(riskIndex)">
            Delete Risk
          </DeleteButton>
        </div>
        <hr />
      </div>

      <AddButton class="margin-button" @click="addRisk()"> Add Risk </AddButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  modelValue: {
    type: Object as PropType<SystemDescriptor>,
    required: true,
  },
});

// Provide hook for parent page to call addGoal. Needed for descriptor import.
const parentAddGoal = () => {
  addGoal();
};

// Provide hook for parent page to call addRisk. Needed for descriptor import.
const parentAddRisk = () => {
  addRisk();
};

// Expose the hooks to parent page.
defineExpose({
  parentAddGoal,
  parentAddRisk,
});

const displaySection = ref<boolean>(true);

// Add GoalDescriptor to goal list.
function addGoal() {
  props.modelValue.goals.push(new GoalDescriptor());
}

/**
 * Delete GoalDescriptor from goal list.
 *
 * @param {number} goalIndex Index of GoalDescriptor to delete
 */
function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    props.modelValue.goals.splice(goalIndex, 1);
  }
}

// Add risk to Risk list.
function addRisk() {
  props.modelValue.risks.push("");
}

/**
 * Delete risk from Risk list.
 *
 * @param {number} riskIndex Index of risk to delete
 */
function deleteRisk(riskIndex: number) {
  if (confirm("Are you sure you want to delete this risk?")) {
    props.modelValue.risks.splice(riskIndex, 1);
  }
}

/**
 * Add MetricDescriptor to list in a goal.
 *
 * @param {number} goalIndex Index of the goal to add a MetricDesriptor to
 */
function addMetric(goalIndex: number) {
  props.modelValue.goals[goalIndex].metrics.push(new MetricDescriptor());
}

/**
 * Delete MetricDescriptor from list in a goal.
 *
 * @param {number} goalIndex Index of goal
 * @param {number} metricIndex Index of MetricDescriptor in goal to delete
 */
function deleteMetric(goalIndex: number, metricIndex: number) {
  if (confirm("Are you sure you want to delete this metric?")) {
    props.modelValue.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}
</script>
