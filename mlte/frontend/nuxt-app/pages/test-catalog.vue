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
const config = useRuntimeConfig();
const token = useCookie("token");

const editFlag = ref(false);
const newEntryFlag = ref(false);
const tagSearchValue = ref("");
const QACategorySearchValue = ref("");
const entryList = ref<TestCatalogEntry[]>([]);
const selectedEntry = ref<TestCatalogEntry>(new TestCatalogEntry());

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
  if (tagSearchValue.value === "" && QACategorySearchValue.value === "") {
    populateFullEntryList();
  } else if (QACategorySearchValue.value === "") {
    await $fetch(config.public.apiPath + "/catalogs/entry/search", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: {
        filter: {
          type: "tag",
          name: "tags",
          value: tagSearchValue.value,
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
  } else if (tagSearchValue.value === "") {
    await $fetch(config.public.apiPath + "/catalogs/entry/search", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: {
        filter: {
          type: "property",
          name: "qa_category",
          value: QACategorySearchValue.value,
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
  } else {
    await $fetch(config.public.apiPath + "/catalogs/entry/search", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
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

async function saveEntry(entry: TestCatalogEntry) {
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
  } catch (exception) {
    console.log("Error in submit.");
    console.log(exception);
    return;
  }

  alert("Entry has been saved successfully.");
  resetSelectedEntry();
  editFlag.value = false;
}
</script>
