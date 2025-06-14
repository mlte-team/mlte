<template>
  <h2 class="section-header">Model Information</h2>
  <div class="input-group">
    <SubHeader>
      Development Compute Resources
      <template #example>
        GPUs = 2, CPUs = 1, Memory = 512 MB, Storage = 1 GB
      </template>
      <template #info>
        Describe the amount and type of compute resources needed for training.
      </template>
    </SubHeader>
    <div>
      <div class="inline-input-left">
        <UsaTextInput
          v-model="props.modelValue.development_compute_resources.gpu"
        >
          <template #label> Graphics Processing Units (GPUs) </template>
        </UsaTextInput>
      </div>

      <div class="inline-input-right">
        <UsaTextInput
          v-model="props.modelValue.development_compute_resources.cpu"
        >
          <template #label> Central Processing Units (CPUs) </template>
        </UsaTextInput>
      </div>
    </div>

    <div>
      <div class="inline-input-left">
        <UsaTextInput
          v-model="props.modelValue.development_compute_resources.memory"
        >
          <template #label> Memory </template>
        </UsaTextInput>
      </div>

      <div class="inline-input-right">
        <UsaTextInput
          v-model="props.modelValue.development_compute_resources.storage"
        >
          <template #label> Storage </template>
        </UsaTextInput>
      </div>
    </div>
  </div>
  <UsaTextarea v-model="props.modelValue.deployment_platform">
    <template #label>
      Deployment Platform
      <InfoIcon>
        Describe the deployment platform for the model, e.g., local server,
        <br />
        cloud server, embedded platform.
        <br />
        <br />
        <i>Example: Local server due to data classification issues.</i>
      </InfoIcon>
    </template>
  </UsaTextarea>

  <UsaTextarea v-model="props.modelValue.capability_deployment_mechanism">
    <template #label>
      Capability Deployment Mechanism
      <InfoIcon>
        Describe how the model capabilities will be made available, <br />
        e.g., API, user facing, data feed.
        <br />
        <br />
        <i
          >Example: The model will expose an API so that it can be called
          <br />
          from the intel analyst UI.</i
        >
      </InfoIcon>
    </template>
  </UsaTextarea>

  <div class="input-group" style="margin-top: 1em">
    <SubHeader>
      Input Specification
      <template #example>
        <UsaTable
          :headers="inputModalHeaders"
          :rows="inputModalRows"
          borderless
          class="table"
        />
      </template>
      <template #info>
        Describe the input data type and format needed for model to conduct
        inference.
      </template>
    </SubHeader>
    <div
      v-for="(inputSpec, inputIndex) in props.modelValue.input_specification"
      :key="inputIndex"
    >
      <h3 class="no-margin-sub-header">Input {{ inputIndex + 1 }}</h3>
      <UsaTextInput v-model="inputSpec.name">
        <template #label>
          Input Name
          <InfoIcon>
            Input name.
            <br />
            <br />
            <i>Example: Audio Recording.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextarea v-model="inputSpec.description">
        <template #label>
          Description
          <InfoIcon>
            Short input description.
            <br />
            <br />
            <i>Example: Audio recording file for matching.</i>
          </InfoIcon>
        </template>
      </UsaTextarea>

      <UsaTextInput v-model="inputSpec.type">
        <template #label>
          Type
          <InfoIcon>
            Input type, e.g., number, string, Boolean, data, image, audio.
            <br />
            <br />
            <i>Example: Audio.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextInput v-model="inputSpec.expected_values">
        <template #label>
          Expected Values
          <InfoIcon>
            Expected values for the input.
            <br />
            <br />
            <i>Example: Non-empty audio file of type WAV, MP3 or MP4.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>
      <DeleteButton class="margin-button" @click="deleteInputSpec(inputIndex)">
        Delete Input
      </DeleteButton>
      <hr />
    </div>
    <AddButton class="margin-button" @click="addInputSpec()">
      Add Additional Input
    </AddButton>
  </div>

  <div class="input-group" style="margin-top: 1em">
    <SubHeader>
      Output Specification
      <template #example>
        <UsaTable
          :headers="outputModalHeaders"
          :rows="outputModalRows"
          borderless
          class="table"
        />
      </template>
      <template #info>
        Describe the output format and specification needed for the system to
        ingest model results.
      </template>
    </SubHeader>
    <div
      v-for="(outputSpec, outputIndex) in props.modelValue.output_specification"
      :key="outputIndex"
    >
      <h3 class="no-margin-sub-header">Output {{ outputIndex + 1 }}</h3>
      <UsaTextInput v-model="outputSpec.name">
        <template #label>
          Output Name
          <InfoIcon>
            Output name.
            <br />
            <br />
            <i>Example: Matching recordings.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextarea v-model="outputSpec.description">
        <template #label>
          Description
          <InfoIcon>
            Short output description.
            <br />
            <br />
            <i>Example: Set of matching recordings from the database.</i>
          </InfoIcon>
        </template>
      </UsaTextarea>

      <UsaTextInput v-model="outputSpec.type">
        <template #label>
          Type
          <InfoIcon>
            Field type, e.g., number, string, Boolean, data, image, audio.
            <br />
            <br />
            <i>
              Example: Vector of Strings with IDs of matching recordings — an
              empty <br />
              vector means that there were no matches.
            </i>
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextInput v-model="outputSpec.expected_values">
        <template #label>
          Expected Values
          <InfoIcon> Expected values for the output. </InfoIcon>
        </template>
      </UsaTextInput>
      <DeleteButton
        class="margin-button"
        @click="deleteOutputSpec(outputIndex)"
      >
        Delete Output
      </DeleteButton>
      <hr />
    </div>
    <AddButton class="margin-button" @click="addOutputSpec()">
      Add Additional Output
    </AddButton>
  </div>

  <div class="input-group" style="margin-top: 1em">
    <SubHeader>
      Production Compute Resources
      <template #example>
        Example: GPUs = 2, CPUs = 2, Memory = 256 MB, Storage = 512 MB
      </template>
      <template #info>
        Describe the amount and type of compute resources needed for inference.
      </template>
    </SubHeader>
    <div>
      <div class="inline-input-left">
        <UsaTextInput
          v-model="props.modelValue.production_compute_resources.gpu"
        >
          <template #label> Graphics Processing Units (GPUs) </template>
        </UsaTextInput>
      </div>

      <div class="inline-input-right">
        <UsaTextInput
          v-model="props.modelValue.production_compute_resources.cpu"
        >
          <template #label> Central Processing Units (CPUs) </template>
        </UsaTextInput>
      </div>
    </div>

    <div>
      <div class="inline-input-left">
        <UsaTextInput
          v-model="props.modelValue.production_compute_resources.memory"
        >
          <template #label> Memory </template>
        </UsaTextInput>
      </div>

      <div class="inline-input-right">
        <UsaTextInput
          v-model="props.modelValue.production_compute_resources.storage"
        >
          <template #label> Storage </template>
        </UsaTextInput>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const props = defineProps({
  modelValue: {
    type: Object as PropType<ModelDescriptor>,
    required: true,
  },
});

const parentAddInputSpec = () => {
  addInputSpec();
};

const parentAddOutputSpec = () => {
  addOutputSpec();
};

defineExpose({
  parentAddInputSpec,
  parentAddOutputSpec,
});

const inputModalHeaders = ref([
  { id: "inputName", label: "Input Name", sortable: false },
  { id: "inputDescription", label: "Input Description", sortable: false },
  { id: "inputType", label: "Input Type", sortable: false },
  { id: "expectedValues", label: "Expected Values", sortable: false },
]);
const inputModalRows = ref([
  {
    id: "audio",
    inputName: "Audio Recording",
    inputDescription: "Audio recording file for matching",
    inputType: "Audio",
    expectedValues: "File of type WAV, MP3, or MP4",
  },
]);

const outputModalHeaders = ref([
  { id: "outputName", label: "Output Name", sortable: false },
  { id: "outputDescription", label: "Output Description", sortable: false },
  { id: "outputType", label: "Output Type", sortable: false },
]);

const outputModalRows = ref([
  {
    id: "recording",
    outputName: "Matching Recordings",
    outputDescription: "Set of matching recordings from the database",
    outputType:
      "Vector of Strings with IDs of matching recordings — an empty vector means that there were no matches",
  },
]);

function addInputSpec() {
  props.modelValue.input_specification.push(new ModelIODescriptor());
}

function deleteInputSpec(specIndex: number) {
  if (confirm("Are you sure you want to delete this spec?")) {
    props.modelValue.input_specification.splice(specIndex, 1);
  }
}

function addOutputSpec() {
  props.modelValue.output_specification.push(new ModelIODescriptor());
}

function deleteOutputSpec(specIndex: number) {
  if (confirm("Are you sure you want to delete this spec?")) {
    props.modelValue.output_specification.splice(specIndex, 1);
  }
}
</script>
