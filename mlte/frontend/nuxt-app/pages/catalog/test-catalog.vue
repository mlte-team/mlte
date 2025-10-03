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
          Search by Quality Attribute
        </label>
        <UsaTextInput v-model="QASearchValue" @keyup.enter="search()" />
      </div>
      <div class="inline-button">
        <UsaButton class="usa-button--unstyled" @click="search()">
          <img src="/assets/uswds/img/usa-icons/search.svg" class="usa-icon" />
        </UsaButton>
      </div>

      <TestCatalogEntryList
        v-model="entryList"
        :catalog-lookup="catalogLookup"
        @edit-entry="editEntry"
        @delete-entry="deleteEntry"
      />
    </div>
    <div v-if="editFlag">
      <TestCatalogEntryEdit
        v-model="selectedEntry"
        :new-entry-flag="newEntryFlag"
        :read-only="
          catalogLookup[selectedEntry.header.catalog_id]
            ? catalogLookup[selectedEntry.header.catalog_id].read_only
            : false
        "
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
const QASearchValue = ref("");
const catalogLookup = ref<Dictionary<CatalogReply>>({});
const entryList = ref<Array<TestCatalogEntry>>([]);
const selectedEntry = ref<TestCatalogEntry>(new TestCatalogEntry());

makeCatalogLookup();
updateFullEntryList();

// Make lookup of catalogs to know if entries are readonly
async function makeCatalogLookup() {
  const catalogList = await getCatalogList();
  catalogList.forEach((catalog: CatalogReply) => {
    catalogLookup.value[catalog.id] = catalog;
  });
}

// Get list of TestCatalogEntry from API and populate page with them.
async function updateFullEntryList() {
  entryList.value = await searchCatalog({
    filter: { type: "all" },
  });
}

// Handle a search query.
async function search() {
  if (tagSearchValue.value === "" && QASearchValue.value === "") {
    updateFullEntryList();
  } else if (QASearchValue.value === "") {
    entryList.value = await searchCatalog({
      filter: { type: "tag", name: "tags", tag: tagSearchValue.value },
    });
  } else if (tagSearchValue.value === "") {
    entryList.value = await searchCatalog({
      filter: {
        type: "property",
        name: "quality_attribute",
        property: QASearchValue.value,
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
            tag: tagSearchValue.value,
          },
          {
            type: "property",
            name: "quality_attribute",
            property: QASearchValue.value,
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
    updateFullEntryList();
  }
}

/**
 * Return to entry list view from the edit view,
 *
 * @param force Cancel the edit without confirmation
 */
function cancelEdit(force: boolean = false) {
  if (
    force ||
    confirm("Are you sure you want to cancel? All changes will be lost.")
  ) {
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
    updateFullEntryList();
    resetSelectedEntry();
    editFlag.value = false;
  }
}
</script>
