<template>
  <div>
    <div v-if="!newEntryFlag">
      <h1 class="section-header">{{ modelValue.header.identifier }}</h1>
      <h3 style="display: inline">Created by:</h3>
      {{ modelValue.header.creator }} - {{ timestamp }}
    </div>
    <div v-if="newEntryFlag">
      <UsaSelect
        v-model="modelValue.header.catalog_id"
        :options="catalogOptions"
        :error="formErrors.catalog"
        @change="formErrors.catalog = false"
      >
        <template #label>
          Catalog
          <InfoIcon> Catalog where test example will be stored. </InfoIcon>
        </template>
        <template #error-message>A catalog must be selected</template>
      </UsaSelect>
      <UsaTextInput
        v-model="props.modelValue.header.identifier"
        :error="formErrors.identifier"
      >
        <template #label>
          Identifier
          <InfoIcon> User-defined identifier for the test example. </InfoIcon>
        </template>
        <template #error-message>Identifier is required.</template>
      </UsaTextInput>
    </div>

    <div class="multi-line-checkbox-div">
      <label class="usa-label">
        Tags
        <InfoIcon>
          System-defined tags that are used in catalog search. Select as many as
          are relevant to the test example.
        </InfoIcon>
      </label>
      <span
        v-for="(tag, tagIndex) in tagOptions"
        :key="tagIndex"
        class="multiple-per-line-checkbox"
      >
        <UsaCheckbox
          v-model="tag.selected"
          @update:model-value="tagChange(tag.selected, tag.name)"
        >
          <template #default>
            {{ tag.name }}
          </template>
        </UsaCheckbox>
      </span>
    </div>

    <!-- Delete when test catalog no longer saves qa category -->
    <UsaSelect
      v-model="modelValue.qa_category"
      :options="QACategoryOptions"
      @change="categoryChange(modelValue.qa_category)"
    >
      <template #label>
        Quality Attribute Category
        <InfoIcon>
          High-level quality attribute category that the test example is
          validating, e.g., functional correctness, performance, robustness.
        </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaSelect>

    <UsaSelect
      v-model="modelValue.quality_attribute"
      :options="selectedQAOptions"
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
    <!-- End of delete section -->

    <!-- Add back when test catalog no longer saves qa category -->
    <!-- <FormFieldsQualityAttributes
       @update-category="props.modelValue.qa_category = $event"
       @update-attribute="props.modelValue.quality_attribute = $event"
     >
      Quality Attribute Category
      <InfoIcon>
        High-level quality attribute category that the test example is 
        validating, e.g., functional correctness, performance, robustness.
      </InfoIcon>
     </FormFieldsQualityAttributes> -->

    <UsaSelect
      v-model="modelValue.code_type"
      :error="formErrors.code_type"
      :options="codeTypeOptions"
      @change="formErrors.code_type = false"
    >
      <template #label>Code Type</template>
      <template #error-message>Code Type must be selected</template>
    </UsaSelect>

    <UsaTextarea
      v-model="modelValue.code"
      style="resize: both; width: 30rem; max-width: 100%"
    >
      <template #label>
        Code
        <InfoIcon> Code for the test example. </InfoIcon>
        <CopyIcon @click="copyCode()" />
      </template>
      <template #error-message>Not defined</template>
    </UsaTextarea>

    <UsaTextarea
      v-model="modelValue.description"
      style="resize: both; width: 30rem; max-width: 100%"
    >
      <template #label>
        Description
        <InfoIcon> Description of the test example. </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaTextarea>

    <UsaTextInput v-model="modelValue.inputs">
      <template #label>
        Inputs
        <InfoIcon>
          Inputs that are required to run the test example, e.g., data sets,
          parameters.
        </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.output">
      <template #label>
        Output
        <InfoIcon>
          Output of the test example, e.g., value, log entry, database entry,
          alert.
        </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="$emit('cancel')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit"> Save </UsaButton>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const emits = defineEmits(["cancel", "submit", "updateEntry"]);
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default() {
      return new TestCatalogEntry();
    },
  },
  newEntryFlag: {
    type: Boolean,
    required: true,
    default: false,
  },
});

const timestamp = ref("");
timestamp.value = new Date(
  props.modelValue.header.created * 1000,
).toLocaleString("en-US");
const formErrors = ref({
  catalog: false,
  identifier: false,
  code_type: false,
});
const catalogOptions = ref<
  {
    value: string;
    text: string;
  }[]
>([]);
const { data: catalogList } = await useFetch<string[]>(
  config.public.apiPath + "/catalogs",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (catalogList.value) {
  catalogList.value.forEach((catalog: object) => {
    if (!catalog.read_only) {
      catalogOptions.value.push({
        value: catalog.id,
        text: catalog.id + " (" + catalog.type.replaceAll("_", " ") + ")",
      });
    }
  });
}

// Delete when test catalog no longer saves qa category
const QACategoryOptions = ref<
  {
    value: string;
    text: string;
    description: string;
    parent: string;
  }[]
>([]);
const { data: QACategoryAPIData } = await useFetch<string[]>(
  config.public.apiPath + "/custom_list/qa_categories/",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (QACategoryAPIData.value) {
  QACategoryAPIData.value.forEach((category: object) => {
    QACategoryOptions.value.push({
      value: category.name,
      text: category.name,
      description: category.description,
      parent: category.parent,
    });
  });
}

const selectedQAOptions = ref([]);
const AllQAOptions = ref<
  {
    value: string;
    text: string;
    description: string;
    parent: string;
  }[]
>([]);
const { data: QAapiOptions } = await useFetch<string[]>(
  config.public.apiPath + "/custom_list/quality_attributes/",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (QAapiOptions.value) {
  QAapiOptions.value.forEach((attribute: object) => {
    AllQAOptions.value.push({
      value: attribute.name,
      text: attribute.name,
      description: attribute.description,
      parent: attribute.parent,
    });
  });
}
// End of delete section

const tagOptions = ref([
  { name: "Audio Analysis", selected: false },
  { name: "Classification", selected: false },
  { name: "Computer Vision", selected: false },
  { name: "Decoder", selected: false },
  { name: "Encoder", selected: false },
  { name: "General", selected: false },
  { name: "Generative Model", selected: false },
  { name: "Infrared", selected: false },
  { name: "NLP", selected: false },
  { name: "Object Detection", selected: false },
  { name: "Sentiment Analysis", selected: false },
  { name: "Regression", selected: false },
  { name: "Segmentation", selected: false },
  { name: "Tabular", selected: false },
  { name: "Time Series", selected: false },
]);

const codeTypeOptions = ref([
  { value: "measurement", text: "Measurement" },
  { value: "validation", text: "Validation " },
]);

tagOptions.value.forEach((tagOption: object) => {
  if (props.modelValue.tags.find((x) => x === tagOption.name)) {
    tagOption.selected = true;
  }
});

// Delete when test catalog no longer saves qa category
// On page load, populate Quality Attribute field if one is selected
categoryChange(
  props.modelValue.qa_category,
  props.modelValue.quality_attribute,
);
// End of delete section

async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (props.modelValue.header.catalog_id === "") {
    formErrors.value.catalog = true;
    inputError = true;
  }

  if (props.modelValue.header.identifier === "") {
    formErrors.value.identifier = true;
    inputError = true;
  }

  if (props.modelValue.code_type === "") {
    formErrors.value.code_type = true;
    inputError = true;
  }

  if (inputError) {
    inputErrorAlert();
    return;
  }

  emit("submit", props.modelValue);
}

function tagChange(selected: boolean, tagOption: object) {
  if (selected) {
    props.modelValue.tags.push(tagOption);
    props.modelValue.tags.sort();
  } else {
    const objForRemoval = props.modelValue.tags.find(
      (x) => x.name === tagOption.name,
    );
    const index = props.modelValue.tags.indexOf(objForRemoval);
    props.modelValue.tags.splice(index, 1);
  }
}
// Delete when test catalog no longer saves qa category
function categoryChange(newCategory: string, quality_attribute?: string) {
  selectedQAOptions.value = [];
  AllQAOptions.value.forEach((attribute: object) => {
    if (attribute.parent == newCategory) {
      selectedQAOptions.value.push(attribute);
    }
  });

  if (typeof quality_attribute === "undefined") {
    props.modelValue.quality_attribute = "";
  } else {
    props.modelValue.quality_attribute = quality_attribute;
  }
}
// End of delete section

function copyCode() {
  navigator.clipboard.writeText(props.modelValue.code);
}
</script>
