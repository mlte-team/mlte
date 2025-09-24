<template>
  <div>
    <UsaSelect
      v-model="qaCategory"
      :options="QACategoryOptions"
      :disabled="props.disabled"
      @change="categoryChange(qaCategory)"
    >
      <template #label>
        <slot />
      </template>
      <template #error-message>Not defined</template>
    </UsaSelect>

    <div v-if="qaCategory === 'Other'">
      <div class="inline-input-left" style="width: 30rem">
        <UsaTextInput v-model="newQACategory">
          <template #label> New Quality Attribute Category </template>
        </UsaTextInput>
      </div>

      <div class="inline-button">
        <UsaButton class="secondary-button" @click="submitCategory">Submit new Category</UsaButton>
      </div>
    </div>

    <UsaSelect
      v-model="qualityAttribute"
      :options="selectedQAOptions"
      :disabled="props.disabled"
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

    <div v-if="qualityAttribute === 'Other'">
      <div class="inline-input-left" style="width: 30rem">
        <UsaTextInput v-model="newQualityAttribute">
          <template #label> New Quality Attribute </template>
        </UsaTextInput>
      </div>

      <div class="inline-button">
        <UsaButton class="secondary-button" @click="submitQA">Submit new Quality Attribute</UsaButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(["updateAttribute"]);
const props = defineProps({
  initialQualityAttribute: {
    type: String,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const qaCategory = ref("");
const newQACategory = ref("");
const qualityAttribute = ref(props.initialQualityAttribute);
const newQualityAttribute = ref("");

const QACategoryOptions = ref<Array<QAOption>>([]);
const selectedQAOptions = ref<Array<QAOption>>([]);
const AllQAOptions = ref<Array<QAOption>>([]);

updateQACategoryOptions();
updateQAOptions();

// On load, populate parent QA Category field if a qualiity attribute is selected
if (props.initialQualityAttribute) {
  const QAapiOptions = await getCustomList("quality_attributes");
  QAapiOptions.forEach((attribute: CustomListEntry) => {
    if (attribute.name === props.initialQualityAttribute) {
      qaCategory.value = attribute.parent;
      categoryChange(qaCategory.value, props.initialQualityAttribute);
    }
  });
}

// Update QA Category Options with categories from the API
async function updateQACategoryOptions() {
  QACategoryOptions.value = [];
  const QACategoryAPIData: Array<CustomListEntry> =
    await getCustomList("qa_categories");

  if (QACategoryAPIData) {
    appendList(QACategoryOptions.value, QACategoryAPIData);
  }
  appendList(QACategoryOptions.value, [new CustomListEntry("Other", "", "")]);
}

// Update QA Options with QA from the API
async function updateQAOptions() {
  AllQAOptions.value = [];
  const QAapiOptions = await getCustomList("quality_attributes");
  if (QAapiOptions) {
    appendList(AllQAOptions.value, QAapiOptions);
  }
  console.log(AllQAOptions.value);
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

  if (newCategory != "Other") {
    selectedQAOptions.value.push(new QAOption("Other", "Other", "", ""));
  }

  if (initialAttrbute === undefined) {
    emit("updateAttribute", "");
  } else {
    emit("updateAttribute", initialAttrbute);
  }
}

/**
 * Append initialList with appendList as QAOption's
 *
 * @param {Array<QAOption>} initialList List of QAOption to be added to, generally empty
 * @param {Array<CustomListEntry>} appendList List of CustomListEntry to add to initialList
 */
function appendList(
  initialList: Array<QAOption>,
  appendList: Array<CustomListEntry>,
) {
  appendList.forEach((entry: CustomListEntry) => {
    initialList.push(
      new QAOption(entry.name, entry.name, entry.description, entry.parent),
    );
  });
}

//
async function submitCategory() {
  const response = await createCustomListEntry(
    "qa_categories",
    new CustomListEntry(newQACategory.value, "", ""),
  );
  if (response) {
    await updateQACategoryOptions();
    qaCategory.value = newQACategory.value;
    categoryChange(newQACategory.value);
    newQACategory.value = "";
  }
}

//
async function submitQA() {
  const response = await createCustomListEntry(
    "quality_attributes",
    new CustomListEntry(newQualityAttribute.value, "", qaCategory.value)
  );
  if (response) {
    await updateQAOptions();
    categoryChange(qaCategory.value);
    qualityAttribute.value = newQualityAttribute.value;
    newQualityAttribute.value = "";
  }
}
</script>
