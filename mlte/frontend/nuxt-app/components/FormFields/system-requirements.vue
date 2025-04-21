<template>
  <h2 class="section-header">System Requirements</h2>
  <p>
    System-dependent requirements and constraints placed on the model under
    development. The fields below correspond to parts of a quality attribute
    scenario, which is a construct used to clearly define system requirements.
    As parts of the scenario are filled in, the corresponding text for the
    scenario will be generated for your validation. Click on the "Example"
    button below for a list of examples.
  </p>

  <div class="input-group">
    <SubHeader :render-info="false">
      Requirements
      <template #example>
        <UsaTable
          :headers="systemModalHeaders"
          :rows="systemModalRows"
          borderless
          class="table"
        />
      </template>
    </SubHeader>
    <div
      v-for="(requirement, requirementIndex) in props.modelValue"
      :key="requirementIndex"
    >
      <h3 class="no-margin-sub-header">
        Requirement {{ requirementIndex + 1 }}
      </h3>
      <p class="input-group" style="padding-top: 10px; padding-bottom: 10px">
        <b>Scenario for {{ requirement.quality }}: </b>
        {{ requirement.stimulus }} from {{ requirement.source }} during
        {{ requirement.environment }}. {{ requirement.response }}
        {{ requirement.measure }}.
      </p>

      <UsaSelect
        v-model="requirement.quality"
        :options="QACategoryOptions"
      >
        <template #label>
          <b>System Quality:</b> What is the model quality attribute category to be tested, such
          as accuracy, performance, robustness, fairness, or resource
          consumption?
          <InfoIcon>
            Quality attribute category by which the model will be evaluated in the context of the
            system <br />
            (e.g., Accuracy, Performance, Robustness, Fairness, Resource
            Consumption).
            <br />
            <br />
            <i>Example: Response time.</i>
          </InfoIcon>
        </template>
      </UsaSelect>

      <UsaTextInput v-model="requirement.stimulus">
        <template #label>
          <b>Stimulus:</b> What is the input to the model, the action, or the
          event that will enable testing of the quality attribute category, such as input data,
          system event, or user operation?
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
      </UsaTextInput>

      <UsaTextInput v-model="requirement.source">
        <template #label>
          <b>Source of Stimulus:</b> Where is the stimulus coming from, such as
          a system component, system user, or data source?
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
      </UsaTextInput>

      <UsaTextInput v-model="requirement.environment">
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
      </UsaTextInput>

      <UsaTextInput v-model="requirement.response">
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
      </UsaTextInput>

      <UsaTextInput v-model="requirement.measure">
        <template #label>
          <b>Response Measure: </b>What is the measure that will determine that
          the correct response has been achieved, such as a statistical
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
      </UsaTextInput>
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
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: [
      {
        quality: "<System Quality>",
        stimulus: "<Stimulus>",
        source: "<Source>",
        environment: "<Environment>",
        response: "<Response>",
        measure: "<Response Measure>",
      },
    ],
  },
});

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

const QACategoryOptions = ref<
  {
    value: string;
    text: string;
    description: string;
    parent: string;
  }[]
>([]);
const { data: QACategoryAPIData } = await useFetch<string[]>(
  config.public.apiPath + "/custom_list/qa_categories/",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
)
if (QACategoryAPIData.value) {
  QACategoryAPIData.value.forEach((category: object) => {
    QACategoryOptions.value.push({
      value: category.name,
      text: category.name,
      description: category.description,
      parent: category.parent,
    })
  })
}

function addRequirement() {
  props.modelValue.push({
    quality: "",
    stimulus: "<Stimulus>",
    source: "<Source>",
    environment: "<Environment>",
    response: "<Response>",
    measure: "<Response Measure>",
  });
}

function deleteRequirement(requirementIndex: number) {
  if (confirm("Are you sure you want to delete this requirement?")) {
    props.modelValue.splice(requirementIndex, 1);
  }
}
</script>
