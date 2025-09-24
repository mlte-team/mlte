<template>
  <div>
    <div v-if="!newEntryFlag">
      <h1 class="section-header">{{ modelValue.name }}</h1>
      <h3 style="display: inline">Custom List:</h3>
      {{ customListName }}
    </div>
    <div v-if="newEntryFlag">
      <UsaSelect
        v-model="selectedCustomList"
        :options="customListOptions"
        @change="updateParentOptions(selectedCustomList)"
      >
        <template #label> Custom List </template>
        <template #error-message>Custom List must be selected.</template>
      </UsaSelect>
      <UsaTextInput v-model="props.modelValue.name" :error="formErrors.name">
        <template #label>Name</template>
        <template #error-message>Name is required.</template>
      </UsaTextInput>
    </div>

    <UsaTextInput v-model="props.modelValue.description">
      <template #label> Description </template>
    </UsaTextInput>

    <UsaSelect
      v-model="props.modelValue.parent"
      :options="parentOptions"
      :error="formErrors.parent"
      :disabled="parentOptions.length == 0"
    >
      <template #label> Parent </template>
      <template #error-message>Parent must be selected.</template>
    </UsaSelect>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="emit('cancel')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit"> Save </UsaButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const emit = defineEmits(["cancel", "submit", "updateEntry"]);
const props = defineProps({
  modelValue: {
    type: Object as PropType<CustomListEntry>,
    required: true,
  },
  newEntryFlag: {
    type: Boolean,
    required: true,
  },
  customListName: {
    type: String,
    required: true,
  },
});

const customListOptions = ref<Array<SelectOption>>([]);
const selectedCustomList = ref<string>("");
const parentOptions = ref<Array<SelectOption>>([]);

const formErrors = ref<Dictionary<boolean>>({
  custom_list: false,
  name: false,
  parent: false,
});

await populateCustomListOptions();
await updateParentOptions(customListOptions.value[0].value);

// Populate list of custom lists to options
async function populateCustomListOptions() {
  const listList = await getCustomListList();
  listList.forEach((list: string) => {
    customListOptions.value.push(new SelectOption(list, list));
  });
}

// Update list of parent Custom List options
async function updateParentOptions(customListId: string) {
  const parentListId = await getCustomListParent(customListId);
  if (parentListId) {
    const parentList = await getCustomList(parentListId);
    parentList.forEach((entry: CustomListEntry) => {
      parentOptions.value.push(new SelectOption(entry.name, entry.name));
    });
  } else {
    parentOptions.value = [];
  }
}

// Handle submission of form.
async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (props.newEntryFlag && selectedCustomList.value === "") {
    formErrors.value.custom_list = true;
    inputError = true;
  }

  if (props.modelValue.name === "") {
    formErrors.value.name = true;
    inputError = true;
  }

  if (props.modelValue.parent === "" && parentOptions.value.length > 0) {
    formErrors.value.parent = true;
    inputError = true;
  }

  if (inputError) {
    inputErrorAlert();
    return;
  }

  if (props.newEntryFlag) {
    emit("submit", selectedCustomList.value, props.modelValue);
  } else {
    emit("submit", props.customListName, props.modelValue);
  }
}
</script>
