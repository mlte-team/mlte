<template>
  <div>
    <UsaSelect
      :model-value="modelValue"
      :options="problemTypeOptions"
      :disabled="props.disabled"
      @update:model-value="emit('update:modelValue', $event)"
    >
      <template #label>
        ML Problem Type
        <InfoIcon>
          Type of ML problem that the model is intended to solve.
          <br />
          <br />
          <i
            >Example: Classification, Clustering, Detection, and others in
            drop-down list.</i
          >
        </InfoIcon>
      </template>
    </UsaSelect>

    <div v-if="modelValue === 'Other'">
      <div class="inline-input-left" style="width: 30rem">
        <UsaTextInput v-model="newProblemType">
          <template #label> New Problem Type </template>
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

const newProblemType = ref("");
const { problemTypeOptions, fetchProblemTypeData } =
  await useProblemTypeOptions();

// Submit new entry to API
async function submit() {
  const response = await createCustomListEntry(
    "problem_types",
    new CustomListEntry(newProblemType.value, "", null),
  );
  if (response) {
    await fetchProblemTypeData();
    emit("update:modelValue", newProblemType.value);
  }
}
</script>
