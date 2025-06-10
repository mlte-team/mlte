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
      @change="$emit('updateAttribute', $event.target.value)"
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
const config = useRuntimeConfig();
const token = useCookie("token");

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
const { data: QACategoryAPIData } = await useFetch<Array<CustomListEntry>>(
  config.public.apiPath + "/custom_list/qa_categories/",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (QACategoryAPIData.value) {
  QACategoryAPIData.value.forEach((category: CustomListEntry) => {
    QACategoryOptions.value.push({
      value: category.name,
      text: category.name,
      description: category.description,
      parent: category.parent,
    });
  });
}

const selectedQAOptions = ref<Array<QAOption>>([]);
const AllQAOptions = ref<Array<QAOption>>([]);
const { data: QAapiOptions } = await useFetch<Array<CustomListEntry>>(
  config.public.apiPath + "/custom_list/quality_attributes/",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (QAapiOptions.value) {
  QAapiOptions.value.forEach((attribute: CustomListEntry) => {
    AllQAOptions.value.push({
      value: attribute.name,
      text: attribute.name,
      description: attribute.description,
      parent: attribute.parent,
    });
  });
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

// initialAttribute is used on startup to set the value of category and parent
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
</script>
