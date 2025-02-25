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
          @update:modelValue="tagChange(tag.selected, tag.name)"
        >
          <template #default>
            {{ tag.name }}
          </template>
        </UsaCheckbox>
      </span>
    </div>

    <UsaSelect
      v-model="modelValue.qa_category"
      :options="QACategoryOptions"
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

    <UsaTextInput v-model="modelValue.quality_attribute">
      <template #label>
        Quality Attribute
        <InfoIcon>
          More specific quality attribute that the test example is validating, e.g.,
          accuracy, inference time, robustness to image blur.
        </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

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

const emit = defineEmits(["cancel", "submit", "updateEntry"]);
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: {
      header: {
        identifier: "",
        creator: "",
        created: -1,
        updated: -1,
        catalog_id: "",
      },
      tags: [],
      qa_category: "",
      quality_attribute: "",
      code_type: "",
      code: "",
      description: "",
      inputs: "",
      output: "",
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
const QACategoryOptions = ref([
  { value: "Explainability", text: "Explainability" },
  { value: "Fairness", text: "Fairness" },
  { value: "Functional Correctness", text: "Functional Correctness" },
  { value: "Interoperability", text: "Interoperability" },
  { value: "Interpretability", text: "Interpretability" },
  { value: "Maintainability", text: "Maintainability" },
  { value: "Monitorability", text: "Monitorability" },
  { value: "Privacy", text: "Privacy" },
  { value: "Resilience", text: "Resilience" },
  { value: "Resource Consumption", text: "Resource Consumption" },
  { value: "Robustness", text: "Robustness" },
  { value: "Safety", text: "Safety" },
  { value: "Scalability", text: "Scalability" },
  { value: "Security", text: "Security" },
  { value: "Testability", text: "Testability" },
  { value: "Trust", text: "Trust" },
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

function copyCode() {
  navigator.clipboard.writeText(props.modelValue.code);
}
</script>
