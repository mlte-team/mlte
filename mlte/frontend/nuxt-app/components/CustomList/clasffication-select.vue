<template>
  <TemplatesCustomListSelect
    :model-value="modelValue"
    :options="classificationOptions"
    :error="formErrors.classification"
    @update:model-value="$emit('update:modelValue', $event)"
    @save-new-entry="submit"
  >
    <template #label> Data Classification </template>
    <template #tooltip>
      What is the classification of the data?
      <br />
      <br />
      <i>Example: Classified, Unclassified, PHI, etc.</i>
    </template>
    <template #new-label> New Data Classification </template>
    <template #error-message>
      New classification must be submitted before form submission.
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

const { classificationOptions, fetchClassificationData } =
  await useClassificationOptions();

const formErrors = inject("formErrors", { classification: false });

// Submit new entry to API
async function submit(newClassification: string) {
  const response = await createCustomListEntry(
    "classification",
    new CustomListEntry(newClassification, "", null),
  );
  if (response) {
    await fetchClassificationData();
    emit("update:modelValue", newClassification);
  }
}
</script>
