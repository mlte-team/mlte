<template>
  <div>
    <TemplatesCustomListSelect
      :model-value="qaCategory"
      :disabled="props.disabled"
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
    </TemplatesCustomListSelect>

    <TemplatesCustomListSelect
      :model-value="props.modelValue"
      :disabled="props.disabled"
      :options="selectedQAOptions"
      @update:model-value="emit('updateAttribute', $event)"
      @save-new-entry="submitQA"
    >
      <template #label> Quality Attribute </template>
      <template #tooltip>
        More specific quality attribute that the test example is validating,
        e.g., accuracy, inference time, robustness to image blur.
      </template>
    </TemplatesCustomListSelect>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(["update:modelValue", "updateAttribute"]);
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

// On load, populate parent QA Category field if a qualiity attribute is selected
if (props.modelValue) {
  AllQAOptions.value.forEach((attribute: QAOption) => {
    if (attribute.text === props.modelValue && attribute.parent) {
      qaCategory.value = attribute.parent;
      categoryChange(qaCategory.value, props.modelValue);
    }
  });
}

/**
 * Handle QA Category change.
 *
 * @param {string} selectedCategory The newly selected category
 * @param {string} [initialAttribute] Optional param to set QA when changing QA Category. Used on startup
 */
function categoryChange(selectedCategory: string, initialAttrbute?: string) {
  qaCategory.value = selectedCategory;
  selectedQAOptions.value = [];
  AllQAOptions.value.forEach((attribute: QAOption) => {
    if (attribute.parent === selectedCategory) {
      selectedQAOptions.value.push(attribute);
    }
  });

  if (selectedCategory != "Other") {
    selectedQAOptions.value.push(new QAOption("Other", "Other", "", ""));
  }

  if (initialAttrbute === undefined) {
    emit("updateAttribute", "");
  } else {
    emit("updateAttribute", initialAttrbute);
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
    qaCategory.value = newCategory;
    categoryChange(newCategory);
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
    emit("updateAttribute", newQA);
  }
}
</script>
