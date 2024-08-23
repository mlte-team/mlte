<template>
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
      v-for="(outputSpec, outputIndex) in $props.modelValue"
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

function addOutputSpec() {
  props.modelValue.push({
    name: "",
    description: "",
    type: "",
    expected_values: "",
  });
}

function deleteOutputSpec(specIndex: number) {
  if (confirm("Are you sure you want to delete this spec?")) {
    props.modelValue.splice(specIndex, 1);
  }
}
</script>
