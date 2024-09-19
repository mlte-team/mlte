<template>
  <div>
    <div v-if="!newEntryFlag">
      <h1 class="section-header">{{ modelValue.header.identifier }}</h1>
      <h3 style="display: inline">Created by:</h3>
      {{ modelValue.header.creator }} - {{ modelValue.header.created }}
    </div>
    <div v-if="newEntryFlag">
      <UsaSelect
        v-model="modelValue.header.catalog_id"
        :options="catalogOptions"
        :error="formErrors.catalog"
        @change="formErrors.catalog = false"
      >
        <template #label>Catalog</template>
        <template #error-message>A catalog must be selected</template>
      </UsaSelect>
      <UsaTextInput
        v-model="props.modelValue.header.identifier"
        :error="formErrors.identifier"
      >
        <template #label>Identifier</template>
        <template #error-message>Identifier is required.</template>
      </UsaTextInput>
    </div>

    <div class="multi-line-checkbox-div">
      <label class="usa-label">Tags</label>
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

    <UsaTextInput
      v-model="modelValue.property_category"
      :error="formErrors.property_category"
    >
      <template #label>Property Category</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.property" :error="formErrors.property">
      <template #label>Property</template>
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

    <UsaTextarea v-model="modelValue.code" :error="formErrors.code">
      <template #label>Code</template>
      <template #error-message>Not defined</template>
    </UsaTextarea>

    <UsaTextInput
      v-model="modelValue.description"
      :error="formErrors.description"
    >
      <template #label>Description</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.inputs" :error="formErrors.inputs">
      <template #label>Inputs</template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.output" :error="formErrors.output">
      <template #label>Ouptut</template>
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
      property_category: "",
      property: "",
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

const formErrors = ref({
  catalog: false,
  identifier: false,
  code_type: false,
});
const catalogOptions = ref<
  {
    value: string,
    text: string,
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
    catalogOptions.value.push({
      value: catalog,
      text: catalog,
    });
  });
}

const codeTypeOptions = ref([
  { value: "measurement", text: "Measurement" },
  { value: "validation", text: "Validation " },
]);
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
</script>
