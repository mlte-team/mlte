<template>
  <TemplatesCollapsibleHeader
    v-model="displaySection"
    @change="displaySection = $event"
  >
    <template #title> System Derived Requirements </template>
  </TemplatesCollapsibleHeader>
  <div v-if="displaySection">
    <div class="input-group">
      <TemplatesSubHeader :render-model="true">
        Requirements
        <template #info>
          <p>
            These are the requirements and constraints derived from the
            ML-enabled system that integrates the model under development. The
            fields below correspond to parts of a quality attribute scenario,
            which is a construct used to clearly define system requirements.
            <br />
            <br />
            As the parts of the scenario are filled in, the corresponding text
            for the scenario will be automatically generated. Edit the fields
            such that the generated scenario corresponds to a coherent
            paragraph; these fields simply ensure that all parts of the scenario
            are considered and form a concrete, testable requirement. Click on
            the "Example" button below for a list of examples.
          </p>
        </template>
        <template #example>
          <UsaTable
            :headers="systemModalHeaders"
            :rows="systemModalRows"
            borderless
            class="table"
          />
        </template>
        <template #buttons>
          <NuxtLink
            target="_blank"
            :to="{
              path: '/etc/quality-model',
            }"
          >
            <UsaButton class="secondary-button"> View Quality Model </UsaButton>
          </NuxtLink>
        </template>
      </TemplatesSubHeader>

      <hr />

      <div
        v-for="(requirement, requirementIndex) in props.modelValue"
        :key="requirementIndex"
      >
        <div class="inline-form-row">
          <h3>Requirement {{ requirementIndex + 1 }}</h3>
          <UsaButton
            class="secondary-button"
            @click="deleteRequirement(requirementIndex)"
          >
            Delete Requirement
          </UsaButton>
        </div>
        <p v-if="requirement.identifier">
          <b>ID: </b> {{ requirement.identifier }}
        </p>
        <p v-else><b>ID: </b> Defined after save</p>
        <p class="input-group" style="padding-top: 10px; padding-bottom: 10px">
          <b>Scenario for {{ requirement.quality }}: </b>
          {{ requirement.stimulus }} {{ requirement.source }}
          {{ requirement.environment }}. {{ requirement.response }}
          {{ requirement.measure }}.
        </p>

        <CustomListQualityAttributeSelect
          :model-value="requirement.quality"
          @update:model-value="requirement.quality = $event"
        >
          <template #label>
            <b>System Quality:</b> What is the model quality attribute category
            to to to be tested, such as accuracy, performance, robustness,
            resource consumption?
          </template>
          <template #tooltip>
            Quality attribute category by which the model will be evaluated in
            the context of the system <br />
            (e.g., Accuracy, Performance, Robustness, Fairness, Resource
            Consumption).
            <br />
            <br />
            <i>Example: Response time.</i>
          </template>
          <template #new-qac-label>New System Quality</template>
        </CustomListQualityAttributeSelect>

        <UsaTextarea v-model="requirement.stimulus">
          <template #label>
            <b>Stimulus:</b> What is the input to the model, the action, or the
            event that will enable testing of the quality attribute category,
            such as input data, system event, or user operation?
            <TemplatesTooltipInfo>
              A condition arriving at the system/model (e.g., data,
              <br />
              event, user operation, attack, request for modification,
              <br />
              completion of a unit of development).
              <br />
              <br />
              <i>Example: Model receives an audio recording.</i>
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.source">
          <template #label>
            <b>Source of Stimulus:</b> Where is the stimulus coming from, such
            as a system component, system user, or data source?
            <TemplatesTooltipInfo>
              Where the stimulus comes from (e.g., data source, <br />
              internal/external user, internal/external component or system,
              <br />
              sensor).
              <br />
              <br />
              <i>Example: Intel analyst application.</i>
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.environment">
          <template #label>
            <b>Environment:</b> What are the conditions under which the scenario
            occurs, such as normal operations, overload conditions, or under
            attack?
            <TemplatesTooltipInfo>
              Set of circumstances in which the scenario takes place <br />
              (e.g., normal operations, overload condition, startup, development
              time).
              <br />
              <br />
              <i>Example: Normal operations.</i>
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.response">
          <template #label>
            <b>Response:</b> What occurs as a result of the stimulus, such as
            inference on the data, event processing, or data validation?
            <TemplatesTooltipInfo>
              Activity that occurs as the result of the arrival of the
              <br />
              stimulus (e.g., inference, process event, deny access, <br />
              implement modification, test).
              <br />
              <br />
              <i>Example: Inference time.</i>
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.measure">
          <template #label>
            <b>Response Measure: </b>What is the measure that will determine
            that the correct response has been achieved, such as a statistical
            property, latency, or execution time?
            <TemplatesTooltipInfo>
              Measures used to determine that the responses enumerated for
              <br />
              the scenario have been achieved (e.g., statistical property,
              <br />
              latency, throughput, execution time, effort).
              <br />
              <br />
              <i>Example: At most 5 seconds.</i>
            </TemplatesTooltipInfo>
          </template>
        </UsaTextarea>
        <hr />
      </div>
      <UsaButton class="secondary-button" @click="addRequirement()">
        Add Requirement
      </UsaButton>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Array<QASDescriptor>,
    required: true,
  },
});

const displaySection = ref<boolean>(true);
const systemModalHeaders = ref([
  { id: "systemQuality", label: "System Quality", sortable: false },
  { id: "stimulus", label: "Stimulus", sortable: false },
  { id: "source", label: "Source of Stimulus", sortable: false },
  { id: "environment", label: "Environment", sortable: false },
  { id: "response", label: "Response", sortable: false },
  { id: "measure", label: "Response Measure", sortable: false },
]);
const systemModalRows = ref([
  {
    id: "fairness",
    systemQuality: "Responsible AI - Fairness",
    stimulus: "The model receives a picture taken at the garden",
    source: "the Garden Buddy application",
    environment: "normal operations",
    response:
      "Regardless of the location in the garden, the model can correctly identify the correct flowers",
    measure: "at least 90% of the time",
  },
  {
    id: "robustness",
    systemQuality: "Continued Operation - Robustness",
    stimulus: "The model receives a picture that is a bit blurry",
    source: "the Garden Buddy application",
    environment: "normal operation",
    response: "the model successfully identifies flowers",
    measure: "at the same rate as non-blurry images",
  },
  {
    id: "explainability",
    systemQuality: "Confidence - Explainability",
    stimulus: "The model receives a picture taken at the garden",
    source: "the Garden Buddy application",
    environment: "normal operations",
    response:
      "The application indicates main features that were used to recognize the flower, as part of the educational experience. ",
    measure:
      "The app displays the original image highlighting the most informative features in flower identification, in addition to the flower name",
  },
  {
    id: "analyzability",
    systemQuality: "Behavior Analysis - Analyzability",
    stimulus:
      "The ML pipeline receives a picture that corresponds to an OOD input",
    source: "the Garden Buddy application",
    environment: "normal operations",
    response: "The model will process the input",
    measure:
      'and the ML pipeline will create a log entry with the tag "Model - Input OOD Error - <Input>, where <Input> is the original input',
  },
]);

// Add QASDescriptor to System Requirements list.
function addRequirement() {
  props.modelValue.push(new QASDescriptor());
}

/**
 * Delete QASDescriptor from System Requrements list.
 *
 * @param {number} Index of QASDescriptor to delete
 */
function deleteRequirement(requirementIndex: number) {
  if (confirm("Are you sure you want to delete this requirement?")) {
    props.modelValue.splice(requirementIndex, 1);
  }
}
</script>
