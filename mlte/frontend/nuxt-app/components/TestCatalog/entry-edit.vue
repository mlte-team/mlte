<template>
  <div>
    <div v-if="!newEntryFlag">
      <h1 class="section-header">{{ modelValue.header.identifier }}</h1>
      <h3 style="display: inline">Created by:</h3>
      {{ modelValue.header.creator }} - {{ modelValue.header.created }}
    </div>
    <div v-if="newEntryFlag">
      <UsaTextInput :error="formErrors.identifier">
        <template #label>Identifier</template>
        <template #error-message>Identifier is required.</template>
      </UsaTextInput>
    </div>

    <div class="multi-line-checkbox-div">
      <label class="usa-label">Tags</label>
      <span
        v-for="(tag, tagIndex) in tagOptions"
        :key="tagIndex"
        class="multiple-per-line-checkbox"
      >
        <UsaCheckbox
          v-model="tag.selected"
          @update:modelValue="tagChange(tag.selected, tag.name)"
        >
          <template #default>
            {{ tag.name }}
          </template>
        </UsaCheckbox>
      </span>
    </div>

    <UsaTextInput
      v-model="modelValue.property_category"
      :error="formErrors.property_category"
    >
      <template #label>Property Category</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.property" :error="formErrors.property">
      <template #label>Property</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.code_type" :error="formErrors.code_type">
      <template #label>Code Type</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextarea v-model="modelValue.code" :error="formErrors.code">
      <template #label>Code</template>
      <template #error-message>Not defined</template>
    </UsaTextarea>

    <UsaTextInput
      v-model="modelValue.description"
      :error="formErrors.description"
    >
      <template #label>Description</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.inputs" :error="formErrors.inputs">
      <template #label>Inputs</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.output" :error="formErrors.output">
      <template #label>Ouptut</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="$emit('cancel')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit"> Save </UsaButton>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const emit = defineEmits(["cancel", "submit", "updateEntry"]);
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: {
      header: {
        identifier: "",
        creator: "",
        created: -1,
        updated: -1,
        catalog_id: "",
      },
      problem_type: [],
      property_category: "",
      property: "",
      code_type: "",
      code: "",
      description: "",
      inputs: "",
      output: "",
    },
  },
  newEntryFlag: {
    type: Boolean,
    required: true,
    default: false,
  },
});

const formErrors = ref({
  identifier: false,
  problem_type: false,
  problem_domain: false,
  property_category: false,
  property: false,
  code_type: false,
  code: false,
  description: false,
  inputs: false,
  output: false,
});
const tagOptions = ref([
  { name: "Audio Analysis", selected: false },
  { name: "Classification", selected: false },
  { name: "Computer Vision", selected: false },
  { name: "Decoder", selected: false },
  { name: "Encoder", selected: false },
  { name: "Generative Model", selected: false },
  { name: "Infrared", selected: false },
  { name: "NLP", selected: false },
  { name: "Object Detection", selected: false },
  { name: "Sentiment Analysis", selected: false },
  { name: "Regression", selected: false },
  { name: "Segmentation", selected: false },
  { name: "Tabular", selected: false },
  { name: "Time Series", selected: false },
]);

tagOptions.value.forEach((tagOption: object) => {
  if (props.modelValue.problem_type.find((x) => x === tagOption.name)) {
    tagOption.selected = true;
  }
});

async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  const inputError = false;

  if (inputError) {
    inputErrorAlert();
    return;
  }

  emit("submit", props.modelValue);
}

function tagChange(selected: boolean, tagOption: object) {
  if (selected) {
    props.modelValue.problem_type.push(tagOption);
  } else {
    const objForRemoval = props.modelValue.problem_type.find(
      (x) => x.name === tagOption.name,
    );
    const index = props.modelValue.problem_type.indexOf(objForRemoval);
    props.modelValue.problem_type.splice(index, 1);
  }
}
</script>
