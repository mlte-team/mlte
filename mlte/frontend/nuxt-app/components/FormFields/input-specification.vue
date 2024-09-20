<template>
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
    <div v-for="(inputSpec, inputIndex) in props.modelValue" :key="inputIndex">
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
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: [
      {
        name: "",
        description: "",
        type: "",
        expected_values: "",
      },
    ],
  },
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

function addInputSpec() {
  props.modelValue.push({
    name: "",
    description: "",
    type: "",
    expected_values: "",
  });
}

function deleteInputSpec(specIndex: number) {
  if (confirm("Are you sure you want to delete this spec?")) {
    props.modelValue.splice(specIndex, 1);
  }
}
</script>
