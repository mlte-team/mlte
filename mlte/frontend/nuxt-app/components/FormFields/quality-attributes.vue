<template>
  <div>
    <UsaSelect
      v-model="qaCategory"
      :options="QACategoryOptions"
      @change="categoryChange(qaCategory)"
    >
      <template #label>
        <slot />
      </template>
      <template #error-message>Not defined</template>
    </UsaSelect>

    <UsaSelect
      v-model="qualityAttribute"
      :options="selectedQAOptions"
      @change="emit('updateAttribute', $event.target.value)"
    >
      <template #label>
        Quality Attribute
        <InfoIcon>
          More specific quality attribute that the test example is validating,
          e.g., accuracy, inference time, robustness to image blur.
        </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaSelect>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(["updateAttribute"]);
const props = defineProps({
  initialQualityAttribute: {
    type: String,
    required: true,
  },
});

const qaCategory = ref("");
const qualityAttribute = ref(props.initialQualityAttribute);

const QACategoryOptions = ref<Array<QAOption>>([]);
const QACategoryAPIData = ref([]);
QACategoryAPIData.value =
  (await useApi("/custom_list/qa_categories/", "GET")) || [];

if (QACategoryAPIData.value) {
  populateList(QACategoryOptions.value, QACategoryAPIData.value);
}

const selectedQAOptions = ref<Array<QAOption>>([]);
const AllQAOptions = ref<Array<QAOption>>([]);
const QAapiOptions = ref<Array<CustomListEntry>>([]);
QAapiOptions.value =
  (await useApi("/custom_list/quality_attributes", "GET")) || [];

if (QAapiOptions.value) {
  populateList(AllQAOptions.value, QAapiOptions.value);
}

// On load, populate parent QA Category field if a qualiity attribute is selected
if (props.initialQualityAttribute) {
  QAapiOptions.value?.forEach((attribute: CustomListEntry) => {
    if (attribute.name === props.initialQualityAttribute) {
      qaCategory.value = attribute.parent;
      categoryChange(qaCategory.value, props.initialQualityAttribute);
    }
  });
}

/**
 * Handle QA Category change.
 *
 * @param {string} newCategory The newly selected category
 * @param {string} [initialAttribute] Optional param to set QA when changing QA Category. Used on startup
 */
function categoryChange(newCategory: string, initialAttrbute?: string) {
  selectedQAOptions.value = [];
  AllQAOptions.value.forEach((attribute: QAOption) => {
    if (attribute.parent === newCategory) {
      selectedQAOptions.value.push(attribute);
    }
  });

  if (initialAttrbute === undefined) {
    emit("updateAttribute", "");
  } else {
    emit("updateAttribute", initialAttrbute);
  }
}

/**
 * Populate initialList with appendList as QAOption's
 *
 * @param {Array<QAOption>} initialList List of QAOption to be added to, generally empty
 * @param {Array<CustomListEntry>} appendList List of CustomListEntry to add to initialList
 */
function populateList(
  initialList: Array<QAOption>,
  appendList: Array<CustomListEntry>,
) {
  appendList.forEach((entry: CustomListEntry) => {
    initialList.push(
      new QAOption(entry.name, entry.name, entry.description, entry.parent),
    );
  });
}
</script>
