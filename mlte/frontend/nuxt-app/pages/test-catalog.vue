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

async function populateFullEntryList() {
  const data: Array<TestCatalogEntry> | null = await useApi(
    "/catalogs/entry/search",
    "POST",
    { body: { filter: { type: "all" } } },
  );
  entryList.value = data || [];
}

async function search() {
  if (tagSearchValue.value === "" && QACategorySearchValue.value === "") {
    populateFullEntryList();
  } else if (QACategorySearchValue.value === "") {
    const data: Array<TestCatalogEntry> | null = await useApi(
      "/catalogs/entry/search",
      "POST",
      {
        body: {
          filter: { type: "tag", name: "tags", value: tagSearchValue.value },
        },
      },
    );
    entryList.value = data || [];
  } else if (tagSearchValue.value === "") {
    const data: Array<TestCatalogEntry> | null = await useApi(
      "/catalogs/entry/search",
      "POST",
      {
        body: {
          filter: {
            type: "property",
            name: "qa_category",
            value: QACategorySearchValue.value,
          },
        },
      },
    );
    entryList.value = data || [];
  } else {
    const data: Array<TestCatalogEntry> | null = await useApi(
      "/catalogs/entry/search",
      "POST",
      {
        body: {
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
        },
      },
    );
    entryList.value = data || [];
  }
}

function resetSelectedEntry() {
  selectedEntry.value = new TestCatalogEntry();
}

function addEntry() {
  resetSelectedEntry();
  editFlag.value = true;
  newEntryFlag.value = true;
}

function editEntry(entry: TestCatalogEntry) {
  selectedEntry.value = entry;
  editFlag.value = true;
  newEntryFlag.value = false;
}

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

  const data = await useApi(
    "/catalog/" + catalogId + "/entry/" + entryId,
    "DELETE",
  );
  if (data) {
    populateFullEntryList();
    successfulSubmission("Entry", entryId, "deleted");
  }
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedEntry();
  }
}

async function saveEntry(entry: TestCatalogEntry) {
  let error = true;

  if (newEntryFlag.value) {
    const data = await useApi(
      "/catalog/" + entry.header.catalog_id + "/entry",
      "POST",
      { body: JSON.stringify(entry) },
    );
    if (data) {
      error = false;
    }
  } else {
    const data = await useApi(
      "catalog/" + entry.header.catalog_id + "/entry",
      "PUT",
      { body: JSON.stringify(entry) },
    );
    if (data) {
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
