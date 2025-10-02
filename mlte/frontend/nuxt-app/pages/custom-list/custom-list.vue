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
 * @param {string} cusotmListName Name of new Custom List to be selected
 */
async function updateList(customListName: string) {
  if (customListName === "") {
    entryList.value = [];
  } else {
    entryList.value = await getCustomList(customListName);
    // Sort by entries by parent
    entryList.value.sort((a, b) => {
      // If there parents are populated, sort by parent then name
      if (a.parent && b.parent) {
        if (a.parent.toLowerCase() < b.parent.toLowerCase()) {
          return -1;
        } else if (a.parent.toLowerCase() > b.parent.toLowerCase()) {
          return 1;
        } else {
          if (a.name.toLowerCase() < b.name.toLowerCase()) {
            return -1;
          } else if (a.name.toLowerCase() > b.name.toLowerCase()) {
            return 1;
          } else {
            return 0;
          }
        }
        // If parent not present, sort by name
      } else {
        if (a.name.toLowerCase() < b.name.toLowerCase()) {
          return -1;
        } else if (a.name.toLowerCase() > b.name.toLowerCase()) {
          return 1;
        } else {
          return 0;
        }
      }
    });
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
 * @param {string} entryId ID of entry to delete
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
 * Save a new or edited custom list entry.
 *
 * @param {string} customListId Custom list to save to
 * @param {CustomListEntry} entry Entry to save
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
