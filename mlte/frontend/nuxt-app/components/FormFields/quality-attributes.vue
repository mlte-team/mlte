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
        <UsaButton class="secondary-button" @click="submitCategory"
          >Save</UsaButton
        >
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
        <UsaButton class="secondary-button" @click="submitQA"> Save </UsaButton>
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

const QACategoryOptions = useQACategoryOptions();
const AllQAOptions = useQualityAttributeOptions();
const selectedQAOptions = ref<Array<QAOption>>([]);

await updateQACategoryOptions();
await updateQAOptions();

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
    new CustomListEntry(newQualityAttribute.value, "", qaCategory.value),
  );
  if (response) {
    await updateQAOptions();
    categoryChange(qaCategory.value, qualityAttribute.value);
    qualityAttribute.value = newQualityAttribute.value;
    emit("updateAttribute", qualityAttribute.value);
    newQualityAttribute.value = "";
  }
}
</script>
