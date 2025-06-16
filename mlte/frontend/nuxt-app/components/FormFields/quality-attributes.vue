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
  addOptionsToList(QACategoryOptions.value, QACategoryAPIData.value);
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
  addOptionsToList(AllQAOptions.value, QAapiOptions.value);
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

function addOptionsToList(
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
