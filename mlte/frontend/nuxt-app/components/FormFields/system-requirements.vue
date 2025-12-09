<template>
  <CollapsibleHeader v-model="displaySection" @change="displaySection = $event">
    <template #title> System Derived Requirements </template>
  </CollapsibleHeader>
  <div v-if="displaySection">
    <div class="input-group">
      <SubHeader>
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
      </SubHeader>

      <hr />

      <div
        v-for="(requirement, requirementIndex) in props.modelValue"
        :key="requirementIndex"
      >
        <h3 class="no-margin-sub-header">
          Requirement {{ requirementIndex + 1 }}
        </h3>
        <p v-if="requirement.identifier">
          <b>ID: </b> {{ requirement.identifier }}
        </p>
        <p v-else><b>ID: </b> Defined after save</p>
        <p class="input-group" style="padding-top: 10px; padding-bottom: 10px">
          <b>Scenario for {{ requirement.quality }}: </b>
          {{ requirement.stimulus }} from {{ requirement.source }} during
          {{ requirement.environment }}. {{ requirement.response }}
          {{ requirement.measure }}.
        </p>

        <FormFieldsQualityAttributes
          :model-value="requirement.quality"
          @update-attribute="requirement.quality = $event"
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
        </FormFieldsQualityAttributes>

        <UsaTextarea v-model="requirement.stimulus" style="height: 5.5rem">
          <template #label>
            <b>Stimulus:</b> What is the input to the model, the action, or the
            event that will enable testing of the quality attribute category,
            such as input data, system event, or user operation?
            <InfoIcon>
              A condition arriving at the system/model (e.g., data,
              <br />
              event, user operation, attack, request for modification,
              <br />
              completion of a unit of development).
              <br />
              <br />
              <i>Example: Model receives an audio recording.</i>
            </InfoIcon>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.source" style="height: 5.5rem">
          <template #label>
            <b>Source of Stimulus:</b> Where is the stimulus coming from, such
            as a system component, system user, or data source?
            <InfoIcon>
              Where the stimulus comes from (e.g., data source, <br />
              internal/external user, internal/external component or system,
              <br />
              sensor).
              <br />
              <br />
              <i>Example: Intel analyst application.</i>
            </InfoIcon>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.environment" style="height: 5.5rem">
          <template #label>
            <b>Environment:</b> What are the conditions under which the scenario
            occurs, such as normal operations, overload conditions, or under
            attack?
            <InfoIcon>
              Set of circumstances in which the scenario takes place <br />
              (e.g., normal operations, overload condition, startup, development
              time).
              <br />
              <br />
              <i>Example: Normal operations.</i>
            </InfoIcon>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.response" style="height: 5.5rem">
          <template #label>
            <b>Response:</b> What occurs as a result of the stimulus, such as
            inference on the data, event processing, or data validation?
            <InfoIcon>
              Activity that occurs as the result of the arrival of the
              <br />
              stimulus (e.g., inference, process event, deny access, <br />
              implement modification, test).
              <br />
              <br />
              <i>Example: Inference time.</i>
            </InfoIcon>
          </template>
        </UsaTextarea>

        <UsaTextarea v-model="requirement.measure" style="height: 5.5rem">
          <template #label>
            <b>Response Measure: </b>What is the measure that will determine
            that the correct response has been achieved, such as a statistical
            property, latency, or execution time?
            <InfoIcon>
              Measures used to determine that the responses enumerated for
              <br />
              the scenario have been achieved (e.g., statistical property,
              <br />
              latency, throughput, execution time, effort).
              <br />
              <br />
              <i>Example: At most 5 seconds.</i>
            </InfoIcon>
          </template>
        </UsaTextarea>
        <DeleteButton
          class="margin-button"
          @click="deleteRequirement(requirementIndex)"
        >
          Delete Requirement
        </DeleteButton>
        <hr />
      </div>
      <AddButton class="margin-button" @click="addRequirement()">
        Add Requirement
      </AddButton>
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
    id: "responseTime",
    systemQuality: "Response Time",
    stimulus: "Model receives an audio recording",
    source: "Intel analyst application",
    environment: "Normal operations",
    response: "Inference time",
    measure: "At most 5 seconds",
  },
  {
    id: "fairness",
    systemQuality: "Fairness - Model Impartial to Photo Location",
    stimulus: "Model receives a picture taken at the garden",
    source: "Flower identification application",
    environment: "Normal operations",
    response: "Correct identification of flowers regardless of garden location",
    measure: "At least 90% of the time",
  },
  {
    id: "robustness",
    systemQuality: "Robustness - Model Robust to Noise (Image Blur)",
    stimulus:
      "Model receives a picture taken at the garden and it is a bit blurry",
    source: "Flower identification application",
    environment: "Normal operations",
    response: "Correct identification of flowers",
    measure: "Same rate as non-blurry images",
  },
  {
    id: "performance",
    systemQuality: "Performance on Operational Platform",
    stimulus: "Model receives a picture taken at a garden",
    source: "Flower identification application",
    environment: "Normal operations",
    response:
      "Model runs on the devices loaned out by the garden centers to visitors. These are small, inexpensive devices with limited CPU power, as well as limited memory and disk space (512 MB and 128 GB, respectively).",
    measure: "No errors due to unavailable resources",
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
