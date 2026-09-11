<template>
  <TemplatesCollapsibleHeader
    v-model="displaySection"
    @change="displaySection = $event"
  >
    <template #title> System Context for Model </template>
  </TemplatesCollapsibleHeader>

  <div v-if="displaySection">
    <div class="input-group">
      <TemplatesSubHeader :render-example="false">
        General Information
        <template #info>
          General information about the problem and usage context.
        </template>
      </TemplatesSubHeader>
      <UsaTextarea v-model="props.modelValue.task">
        <template #label>
          ML Task
          <TemplatesTooltipInfo>
            Well-defined task that model is expected to perform, or problem that
            the model is expected to solve.
            <br />
            <br />
            <i>Example: Match voice recordings spoken by the same person.</i>
          </TemplatesTooltipInfo>
        </template>
      </UsaTextarea>

      <CustomListProblemTypeSelect v-model="props.modelValue.problem_type" />

      <UsaTextarea v-model="props.modelValue.usage_context">
        <template #label>
          Usage Context for the Model
          <TemplatesTooltipInfo>
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
          </TemplatesTooltipInfo>
        </template>
      </UsaTextarea>
    </div>

    <div class="input-group">
      <TemplatesSubHeader :render-example="false">
        Goals
        <template #info>
          Goals or objectives that the model is going to help satisfy as part of
          the system.
        </template>
      </TemplatesSubHeader>

      <hr />

      <div v-for="(goal, goalIndex) in props.modelValue.goals" :key="goalIndex">
        <div class="inline-form-row">
          <h3>Goal {{ goalIndex + 1 }}</h3>
          <UsaButton class="delete-button" @click="deleteGoal(goalIndex)">
            Delete Goal {{ goalIndex + 1 }}
          </UsaButton>
        </div>
        <UsaTextarea v-model="goal.description">
          <template #label>
            Goal Description
            <TemplatesTooltipInfo>
              Short description for the goal.
              <br />
              <br />
              <i
                >Example: Identify voice recordings that belong to a given
                person of interest.</i
              >
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>

        <TemplatesSubHeader :render-example="false" :render-info="false">
          Metrics
        </TemplatesSubHeader>
        <div
          v-for="(metric, metricIndex) in goal.metrics"
          :key="metricIndex"
          class="inline-form-row"
        >
          <div class="grid-col-5">
            <UsaTextInput v-model="metric.description">
              <template #label>
                Description
                <TemplatesTooltipInfo>
                  Performance metric that captures the system's ability to
                  accomplish the goal,<br />
                  i.e., acceptance criteria for determining that the model is
                  performing correctly.
                  <br />
                  <br />
                  <i>Example: Accuracy > 90%</i>
                </TemplatesTooltipInfo>
              </template>
            </UsaTextInput>
          </div>

          <div class="grid-col-5">
            <UsaTextInput v-model="metric.baseline">
              <template #label>
                Baseline Source
                <TemplatesTooltipInfo>
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
                </TemplatesTooltipInfo>
              </template>
            </UsaTextInput>
          </div>
          <div class="grid-col-2">
            <UsaButton
              class="delete-button"
              @click="deleteMetric(goalIndex, metricIndex)"
            >
              Delete Metric
            </UsaButton>
          </div>
        </div>
        <UsaButton class="secondary-button" @click="addMetric(goalIndex)">
          Add Metric
        </UsaButton>
        <hr />
      </div>

      <UsaButton class="secondary-button" @click="addGoal()">
        Add Goal
      </UsaButton>
    </div>

    <div class="input-group">
      <TemplatesSubHeader :render-example="false">
        Risks
        <template #info>
          Risks to model performance such as false positives, false negatives,
          hallucinations, or bias.
        </template>
      </TemplatesSubHeader>

      <hr />

      <div v-for="(risk, riskIndex) in props.modelValue.risks" :key="riskIndex">
        <div class="inline-form-row">
          <h3>Risk {{ riskIndex + 1 }}</h3>
          <UsaButton class="delete-button" @click="deleteRisk(riskIndex)">
            Delete Risk {{ riskIndex + 1 }}
          </UsaButton>
        </div>
        <UsaTextarea v-model="props.modelValue.risks[riskIndex]">
          <template #label>
            Risk
            <TemplatesTooltipInfo>
              Short description for the risk.
              <br />
              <br />
              <i>
                Example: Model may not indicate proper results if data is out
                bounds.
              </i>
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>
        <hr />
      </div>

      <UsaButton class="secondary-button" @click="addRisk()">
        Add Risk
      </UsaButton>
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
 * @param {number} goalIndex Index of the goal to add a MetricDescriptor to
 */
function addMetric(goalIndex: number) {
  const goal = props.modelValue?.goals?.[goalIndex];
  if (goal) {
    goal.metrics ??= [];
    goal.metrics.push(new MetricDescriptor());
  }
}

/**
 * Delete MetricDescriptor from list in a goal.
 *
 * @param {number} goalIndex Index of goal
 * @param {number} metricIndex Index of MetricDescriptor in goal to delete
 */
function deleteMetric(goalIndex: number, metricIndex: number) {
  const metrics = props.modelValue?.goals?.[goalIndex]?.metrics;
  if (metrics && confirm("Are you sure you want to delete this metric?")) {
    metrics.splice(metricIndex, 1);
  }
}
</script>
