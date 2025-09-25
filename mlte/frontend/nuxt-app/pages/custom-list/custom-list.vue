<template>
  <NuxtLayout name="base-layout">
    <title>Custom Lists</title>
    <template #page-title>Custom Lists</template>

    <div v-if="!editFlag">
      <UsaButton
        class="secondary-button sub-header-float-button"
        @click="addEntry"
      >
        Add Entry
      </UsaButton>
      <div class="inline-input-left">
        <UsaSelect
          v-model="selectedCustomList"
          :options="customListOptions"
          @change="updateList(selectedCustomList)"
        />
      </div>

      <CustomListEntryList
        v-model="entryList"
        @edit-entry="editEntry"
        @delete-entry="deleteEntry"
      />
    </div>
    <div v-if="editFlag">
      <CustomListEntryEdit
        v-model="selectedEntry"
        :new-entry-flag="newEntryFlag"
        :initial-custom-list-name="selectedCustomList"
        :custom-list-options="customListOptions"
        @cancel="cancelEdit"
        @submit="saveEntry"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const editFlag = ref(false);
const newEntryFlag = ref(false);

const { customListOptions } = await useCustomListOptions();
const selectedCustomList = ref<string>("");
const entryList = ref<Array<CustomListEntry>>([]);
const selectedEntry = ref<CustomListEntry>(new CustomListEntry());

pageSetup();

// Select an initial list on page load
async function pageSetup() {
  if (customListOptions.value.length > 0) {
    selectedCustomList.value = customListOptions.value[0].value;
    updateList(customListOptions.value[0].value);
  }
}

/**
 * Update the list of Custom List Entries being displayed.
 *
 * @param {string} Name of new Custom List to be selected
 */
async function updateList(customListName: string) {
  if (customListName === "") {
    entryList.value = [];
  } else {
    entryList.value = await getCustomList(customListName);
  }
}

// Reset selectedEntry, for example when an edit is completed.
function resetSelectedEntry() {
  selectedEntry.value = new CustomListEntry();
}

// Switch to the edit entry view with newEntryFlag enabled.
function addEntry() {
  resetSelectedEntry();
  editFlag.value = true;
  newEntryFlag.value = true;
}

// Switch to the edit entry view with newEntryFlag disabled.
function editEntry(entry: CustomListEntry) {
  selectedEntry.value = entry;
  editFlag.value = true;
  newEntryFlag.value = false;
}

/**
 * Delete a Custom List entry,
 *
 * @param {string}
 */
async function deleteEntry(entryId: string) {
  if (!confirm("Are you sure you want to delete the entry: " + entryId + "?")) {
    return;
  }

  const response = await deleteCustomListEntry(
    selectedCustomList.value,
    entryId,
  );
  if (response) {
    updateList(selectedCustomList.value);
  }
}

// Return to entry list view from the edit view.
function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedEntry();
  }
}

/**
 *
 */
async function saveEntry(customListId: string, entry: CustomListEntry) {
  let error = true;

  if (newEntryFlag.value) {
    const response = await createCustomListEntry(customListId, entry);
    if (response) {
      error = false;
    }
  } else {
    const response = await updateCustomListEntry(customListId, entry);
    if (response) {
      error = false;
    }
  }

  if (!error) {
    updateList(selectedCustomList.value);
    resetSelectedEntry();
    editFlag.value = false;
  }
}
</script>
