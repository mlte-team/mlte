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

    <!-- <UsaTextInput
      v-model="modelValue.problem_type"
      :error="formErrors.problem_type"
    >
      <template #label>Problem Type @@ Should be list? @@</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput
      v-model="modelValue.problem_domain"
      :error="formErrors.problem_domain"
    >
      <template #label>Problem Domain @@ Should be list? @@</template>
      <template #error-message>Not defined</template>
    </UsaTextInput> -->

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
      problem_domain: [],
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
const codeTypeOptions = ref([]);

async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  const inputError = false;

  if (inputError) {
    inputErrorAlert();
    return;
  }

  emit("submit", props.modelValue);
}
</script>
