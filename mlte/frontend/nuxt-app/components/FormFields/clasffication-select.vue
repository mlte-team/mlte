<template>
  <div>
    <UsaSelect
      :model-value="modelValue"
      :options="classificationOptions"
      :disabled="props.disabled"
      @update:model-value="emit('update:modelValue', $event)"
    >
      <template #label>
        Data Classification
        <InfoIcon>
          What is the classification of the data?
          <br />
          <br />
          <i>Example: Classified, Unclassified, PHI, etc.</i>
        </InfoIcon>
      </template>
    </UsaSelect>

    <div v-if="modelValue === 'Other'">
      <div class="inline-input-left" style="width: 30rem">
        <UsaTextInput v-model="newClassification">
          <template #label> New Classification </template>
        </UsaTextInput>
      </div>

      <div class="inline-button">
        <UsaButton class="secondary-button" @click="submit"> Save </UsaButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(["update:modelValue"]);
const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const newClassification = ref("");
const { classificationOptions, fetchClassificationData } =
  await useClassificationOptions();

// Submit new entry to API
async function submit() {
  const response = await createCustomListEntry(
    "classification",
    new CustomListEntry(newClassification.value, "", null),
  );
  if (response) {
    await fetchClassificationData();
    emit("update:modelValue", newClassification.value);
  }
}
</script>
