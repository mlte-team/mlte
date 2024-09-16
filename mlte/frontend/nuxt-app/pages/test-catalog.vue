<template>
  <NuxtLayout name="base-layout">
    <title>Test Catalog</title>
    <template #page-title>Test Catalog</template>
    <template #right-sidebar>
      <div>
        <div v-if="!editFlag">
          <UsaButton class="secondary-button" @click="addEntry">
            New Catalog Entry
          </UsaButton>
        </div>
      </div>
    </template>

    <div v-if="!editFlag">
      <div class="inline-input-right">
        <UsaTextInput v-model="searchValue" @keyup.enter="search()">
          <template #label> Search by Identifier </template>
        </UsaTextInput>
      </div>
      <div class="inline-button">
        <UsaButton class="usa-button--unstyled" @click="search()">
          <img src="/assets/uswds/img/usa-icons/search.svg" class="usa-icon" />
        </UsaButton>
      </div>

      <TestCatalogEntryList
        v-model="entryList"
        @editEntry="editEntry"
        @deleteEntry="deleteEntry"
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
const config = useRuntimeConfig();
const token = useCookie("token");

const editFlag = ref(false);
const newEntryFlag = ref(false);
const searchValue = ref("");
const entryList = ref<{
  header: object;
  problem_type: Array<string>;
  problem_domain: Array<string>;
  property_category: string;
  property: string;
  code_type: string;
  code: string;
  description: string;
  inputs: string;
  output: string;
}>([]);
const selectedEntry = ref({});

populateFullEntryList();

async function populateFullEntryList() {
  await $fetch(config.public.apiPath + "/catalogs/entry/search", {
    retry: 0,
    method: "POST",
    headers: {
      Authorization: "Bearer " + token.value,
    },
    body: {
      filter: {
        type: "all",
      },
    },
    onRequestError() {
      requestErrorAlert();
    },
    onResponse({ response }) {
      if (response.ok) {
        entryList.value = response._data;
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });
}

async function search() {
  if (searchValue.value === "") {
    populateFullEntryList();
  } else {
    await $fetch(config.public.apiPath + "/catalogs/entry/search", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: {
        filter: {
          type: "identifier",
          id: searchValue.value,
        },
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          entryList.value = response._data;
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    });
  }
}

function resetSelectedEntry() {
  selectedEntry.value = {
    header: {
      identifier: "",
      creator: "",
      created: -1,
      updated: -1,
      catalog_id: "",
    },
    problem_type: [],
    problem_domain: [],
    property_category: "",
    property: "",
    code_type: "",
    code: "",
    description: "",
    inputs: "",
    output: "",
  };
}

function addEntry() {
  resetSelectedEntry();
  editFlag.value = true;
  newEntryFlag.value = true;
}

function editEntry(entry: object) {
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

  await $fetch(
    config.public.apiPath + "/catalog/" + catalogId + "/entry/" + entryId,
    {
      retry: 0,
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          populateFullEntryList();
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    },
  );
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedEntry();
  }
}

async function saveEntry(entry: object) {
  try {
    if (newEntryFlag.value) {
      await $fetch(
        config.public.apiPath +
          "/catalog/" +
          entry.header.catalog_id +
          "/entry",
        {
          retry: 0,
          method: "POST",
          headers: {
            Authorization: "Bearer " + token.value,
          },
          body: entry,
          onRequestError() {
            requestErrorAlert();
          },
          onResponse({ response }) {
            if (response.ok) {
              populateFullEntryList();
            }
          },
          onResponseError({ response }) {
            handleHttpError(response.status, response._data.error_description);
          },
        },
      );
    } else {
      await $fetch(
        config.public.apiPath +
          "/catalog/" +
          entry.header.catalog_id +
          "/entry",
        {
          retry: 0,
          method: "PUT",
          headers: {
            Authorization: "Bearer " + token.value,
          },
          body: entry,
          onRequestError() {
            requestErrorAlert();
          },
          onResponse({ response }) {
            if (response.ok) {
              populateFullEntryList();
            }
          },
          onResponseError({ response }) {
            handleHttpError(response.status, response._data.error_description);
          },
        },
      );
    }
  } catch {
    console.log("Error in submit.");
    return;
  }

  alert("Entry has been saved successfully.");
  resetSelectedEntry();
  editFlag.value = false;
}
</script>
