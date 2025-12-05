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
          :disabled="props.readOnly"
          @update:model-value="tagChange(tag.selected, tag.name)"
        >
          <template #default>
            {{ tag.name }}
          </template>
        </UsaCheckbox>
      </span>
    </div>

    <FormFieldsQualityAttributes
      :initial-quality-attribute="props.modelValue.quality_attribute"
      :disabled="props.readOnly"
      @update-attribute="props.modelValue.quality_attribute = $event"
    >
      Quality Attribute Category
      <InfoIcon>
        High-level quality attribute category that the test example is
        validating, e.g., functional correctness, performance, robustness.
      </InfoIcon>
    </FormFieldsQualityAttributes>

    <label class="usa-label">
      Code
      <InfoIcon> Code for the test example. </InfoIcon>
      <CopyIcon @click="copyCode()" />
    </label>
    <Codemirror
      v-model="modelValue.code"
      :disabled="props.readOnly"
      :style="{ height: '35ch' }"
      :extensions="extensions"
    />

    <UsaTextarea
      v-model="modelValue.description"
      :disabled="props.readOnly"
      style="resize: both; width: 30rem; max-width: 100%"
    >
      <template #label>
        Description
        <InfoIcon> Description of the test example. </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaTextarea>

    <UsaTextInput v-model="modelValue.inputs" :disabled="props.readOnly">
      <template #label>
        Inputs
        <InfoIcon>
          Inputs that are required to run the test example, e.g., data sets,
          parameters.
        </InfoIcon>
      </template>
      <template #error-message>Not defined</template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.output" :disabled="props.readOnly">
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
      <template v-if="props.readOnly">
        <UsaButton class="primary-button" @click="emit('cancel', true)">
          Back
        </UsaButton>
      </template>
      <template v-else>
        <UsaButton class="primary-button" @click="emit('cancel')">
          Cancel
        </UsaButton>
        <UsaButton class="primary-button" @click="submit"> Save </UsaButton>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
const extensions = [python()];

const emit = defineEmits(["cancel", "submit", "updateEntry"]);
const props = defineProps({
  modelValue: {
    type: Object as PropType<TestCatalogEntry>,
    required: true,
  },
  newEntryFlag: {
    type: Boolean,
    required: true,
  },
  readOnly: {
    type: Boolean,
    required: true,
  },
});

const timestamp = ref("");
timestamp.value = new Date(
  props.modelValue.header.created * 1000,
).toLocaleString("en-US");
const formErrors = ref<Dictionary<boolean>>({
  catalog: false,
  identifier: false,
});
const catalogOptions = ref<Array<SelectOption>>([]);
const { tagOptions } = await useTagOptions();

await updateQAData();
populateCatalogOptions();
tagOptions.value.forEach((tagOption: CheckboxOption) => {
  if (props.modelValue.tags.find((x) => x === tagOption.name)) {
    tagOption.selected = true;
  } else {
    tagOption.selected = false;
  }
});

async function populateCatalogOptions() {
  const catalogList = await getCatalogList();
  if (catalogList) {
    catalogList.forEach((catalog: CatalogReply) => {
      if (!catalog.read_only) {
        catalogOptions.value.push(
          new SelectOption(
            catalog.id,
            catalog.id + " (" + catalog.type.replaceAll("_", " ") + ")",
          ),
        );
      }
    });
  }
}

// Handle submission of form.
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

  if (inputError) {
    inputErrorAlert();
    return;
  }

  emit("submit", props.modelValue);
}

/**
 * Handle a tag change either adding the item to selections, or removing it.
 *
 * @param {boolean} selected Flag indicating if item was selected or deselected
 * @param {string} tagName Tag that was selected or deselected
 */
function tagChange(selected: boolean, tagName: string) {
  if (selected) {
    props.modelValue.tags.push(tagName);
    props.modelValue.tags.sort();
  } else {
    const objForRemoval = props.modelValue.tags.find(
      (x: string) => x === tagName,
    );
    // TODO : Add error handling
    if (objForRemoval) {
      const index = props.modelValue.tags.indexOf(objForRemoval);
      props.modelValue.tags.splice(index, 1);
    }
  }
}

// Copies contents of code form field to the clipboard.
function copyCode() {
  navigator.clipboard.writeText(props.modelValue.code);
}
</script>
