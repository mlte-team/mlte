<template>
  <div>
    <TemplatesCustomListSelect
      :model-value="qaCategory"
      :disabled="props.disabled"
      :error="formErrors.qa"
      :options="QACategoryOptions"
      @update:model-value="categoryChange($event)"
      @save-new-entry="submitCategory"
    >
      <template #label>
        <slot name="label" />
      </template>
      <template #tooltip>
        <slot name="tooltip" />
      </template>
      <template #new-label>
        <slot name="new-qac-label" />
      </template>
      <template #error-message>
        New quality attribute category must be submitted before form submission.
      </template>
    </TemplatesCustomListSelect>

    <TemplatesCustomListSelect
      :model-value="props.modelValue"
      :disabled="props.disabled || qaCategory === 'Other'"
      :error="formErrors.qa"
      :options="selectedQAOptions"
      @update:model-value="emit('update:modelValue', $event)"
      @save-new-entry="submitQA"
    >
      <template #label> Quality Attribute </template>
      <template #tooltip>
        More specific quality attribute that the test example is validating,
        e.g., accuracy, inference time, robustness to image blur.
      </template>
      <template #new-label> New Quality Attribute </template>
      <template #error-message>
        New quality attribute must be submitted before form submission.
      </template>
    </TemplatesCustomListSelect>
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

const qaCategory = ref("");

const { QACategoryOptions, fetchQACData } = await useQACategoryOptions();
const { qualityAttributeOptions: AllQAOptions, fetchQAData } =
  await useQualityAttributeOptions();
const selectedQAOptions = ref<Array<QAOption>>([]);

const formErrors = inject("formErrors", { qa: false });

// Helper to update options list based on selected category
function updateQAOptions(category: string) {
  selectedQAOptions.value = AllQAOptions.value.filter(
    (attribute: QAOption) => attribute.parent === category,
  );
  if (category && category !== "Other") {
    selectedQAOptions.value.push(new QAOption("Other", "Other", "", ""));
  }
}

// Watch modelValue to reactively update local state when parent props change
watch(
  () => props.modelValue,
  (newVal) => {
    if (!newVal) {
      qaCategory.value = "";
      selectedQAOptions.value = [];
      return;
    }

    const matchingQA = AllQAOptions.value.find(
      (attribute: QAOption) => attribute.text === newVal && attribute.parent,
    );

    if (matchingQA && matchingQA.parent) {
      qaCategory.value = matchingQA.parent;
      updateQAOptions(matchingQA.parent);
    }
  },
  { immediate: true },
);

/**
 * Handle QA Category change.
 *
 * @param {string} selectedCategory The newly selected category
 * @param {string} [selectedAttribute] Optional param to set QA when changing QA Category
 */
function categoryChange(selectedCategory: string, selectedAttribute?: string) {
  qaCategory.value = selectedCategory;
  updateQAOptions(selectedCategory);

  if (selectedCategory === "Other") {
    // Value set to "Other" implies that a category addition is in progress, and should cause an error on submit.
    emit("update:modelValue", "Other");
  } else if (selectedAttribute === undefined) {
    emit("update:modelValue", "");
  } else {
    emit("update:modelValue", selectedAttribute);
  }
}

// Submit new QA Category to API
async function submitCategory(newCategory: string) {
  const response = await createCustomListEntry(
    "qa_categories",
    new CustomListEntry(newCategory, "", null),
  );
  if (response) {
    await fetchQACData();
    categoryChange(newCategory, "Other");
  }
}

// Submit new QA to API
async function submitQA(newQA: string) {
  const response = await createCustomListEntry(
    "quality_attributes",
    new CustomListEntry(newQA, "", qaCategory.value),
  );
  if (response) {
    await fetchQAData();
    categoryChange(qaCategory.value, props.modelValue);
    emit("update:modelValue", newQA);
  }
}
</script>
