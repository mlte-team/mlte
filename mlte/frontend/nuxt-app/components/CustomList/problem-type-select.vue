<template>
  <TemplatesCustomListSelect
    :model-value="modelValue"
    :options="problemTypeOptions"
    :error="formErrors.problem_type"
    @update:model-value="$emit('update:modelValue', $event)"
    @save-new-entry="submit"
  >
    <template #label> ML Problem Type </template>
    <template #tooltip>
      Type of ML problem that the model is intended to solve.
      <br />
      <br />
      <i>
        Example: Classification, Clustering, Detection, and others in drop-down
        list.
      </i>
    </template>
    <template #new-label> New Problem Type </template>
    <template #error-message>
      New problem type must be submitted before form submission.
    </template>
  </TemplatesCustomListSelect>
</template>

<script setup lang="ts">
const emit = defineEmits(["update:modelValue"]);
const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
});

const { problemTypeOptions, fetchProblemTypeData } =
  await useProblemTypeOptions();

const formErrors = inject("formErrors", { problem_type: false });

// Submit new entry to API
async function submit(newProblemType: string) {
  const response = await createCustomListEntry(
    "problem_types",
    new CustomListEntry(newProblemType, "", null),
  );
  if (response) {
    await fetchProblemTypeData();
    emit("update:modelValue", newProblemType);
  }
}
</script>
