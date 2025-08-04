<template>
  <NuxtLayout name="base-layout">
    <title>Test Catalog</title>
    <template #page-title>Test Catalog</template>

    <div v-if="!editFlag">
      <UsaButton
        class="secondary-button sub-header-float-button"
        @click="addEntry"
      >
        Add Catalog Entry
      </UsaButton>
      <div class="inline-input-left">
        <label class="usa-label" style="margin-top: 0px"> Search by Tag </label>
        <UsaTextInput v-model="tagSearchValue" @keyup.enter="search()" />
      </div>

      <div class="inline-input-right">
        <label class="usa-label" style="margin-top: 0px">
          Search by Quality Attribute Category
        </label>
        <UsaTextInput v-model="QACategorySearchValue" @keyup.enter="search()" />
      </div>
      <div class="inline-button">
        <UsaButton class="usa-button--unstyled" @click="search()">
          <img src="/assets/uswds/img/usa-icons/search.svg" class="usa-icon" />
        </UsaButton>
      </div>

      <TestCatalogEntryList
        v-model="entryList"
        @edit-entry="editEntry"
        @delete-entry="deleteEntry"
      />
    </div>
    <div v-if="editFlag">
      <TestCatalogEntryEdit
        v-model="selectedEntry"
        :new-entry-flag="newEntryFlag"
        @cancel="cancelEdit"
        @submit="saveEntry"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const editFlag = ref(false);
const newEntryFlag = ref(false);
const tagSearchValue = ref("");
const QACategorySearchValue = ref("");
const entryList = ref<TestCatalogEntry[]>([]);
const selectedEntry = ref<TestCatalogEntry>(new TestCatalogEntry());

populateFullEntryList();

// Get list of TestCatalogEntry from API and populate page with them.
async function populateFullEntryList() {
  entryList.value = await searchCatalog({
    filter: { type: "all" },
  });
}

// Handle a search query.
async function search() {
  if (tagSearchValue.value === "" && QACategorySearchValue.value === "") {
    populateFullEntryList();
  } else if (QACategorySearchValue.value === "") {
    entryList.value = await searchCatalog({
      filter: { type: "tag", name: "tags", value: tagSearchValue.value },
    });
  } else if (tagSearchValue.value === "") {
    entryList.value = await searchCatalog({
      filter: {
        type: "property",
        name: "qa_category",
        value: QACategorySearchValue.value,
      },
    });
  } else {
    entryList.value = await searchCatalog({
      filter: {
        type: "and",
        filters: [
          {
            type: "tag",
            name: "tags",
            value: tagSearchValue.value,
          },
          {
            type: "property",
            name: "qa_category",
            value: QACategorySearchValue.value,
          },
        ],
      },
    });
  }
}

// Reset selectedEntry, for example when an edit is completed.
function resetSelectedEntry() {
  selectedEntry.value = new TestCatalogEntry();
}

// Switch to the edit entry view with newEntryFlag enabled.
function addEntry() {
  resetSelectedEntry();
  editFlag.value = true;
  newEntryFlag.value = true;
}

// Switch to the edit entry view with newEntryFlag disabled.
function editEntry(entry: TestCatalogEntry) {
  selectedEntry.value = entry;
  editFlag.value = true;
  newEntryFlag.value = false;
}

/**
 * Delete a TestCatalogEntry
 *
 * @param {string} catalogId Catalog containing the TestCatalogEntry to be deleted
 * @param {string} entryId ID of the TestCatalogEntry to be deleted
 */
async function deleteEntry(catalogId: string, entryId: string) {
  if (
    !confirm(
      "Are you sure you want to delete the entry: " +
        entryId +
        " in the " +
        catalogId +
        " catalog?",
    )
  ) {
    return;
  }

  const response = await deleteCatalogEntry(catalogId, entryId);
  if (response) {
    populateFullEntryList();
    successfulSubmission("Entry", entryId, "deleted");
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
 * Save new entry, or save changes to entry.
 *
 * @param {TestCatalogEntry} entry TestCatalogEntry to be saved
 */
async function saveEntry(entry: TestCatalogEntry) {
  let error = true;

  if (newEntryFlag.value) {
    const response = await createCatalogEntry(entry.header.catalog_id, entry);
    if (response) {
      error = false;
    }
  } else {
    const response = await updateCatalogEntry(entry.header.catalog_id, entry);
    if (response) {
      error = false;
    }
  }

  if (!error) {
    populateFullEntryList();
    resetSelectedEntry();
    editFlag.value = false;
    successfulSubmission("Entry", entry.header.identifier, "saved");
  }
}
</script>
