<template>
  <NuxtLayout name="base-layout">
    <title>Manage Groups</title>
    <template #page-title>Manage Groups</template>

    <div v-if="!editFlag">
      <UsaButton class="secondary-button" @click="addGroup" style="float: right;">
        Add Group
      </UsaButton>
      <AdminGroupList
        v-model="groupList"
        @editGroup="editGroup"
        @deleteGroup="deleteGroup"
      />
    </div>
    <div v-if="editFlag">
      <AdminGroupEdit
        v-model="selectedGroup"
        :new-group-flag="newGroupFlag"
        @cancel="cancelEdit"
        @submit="saveGroup"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const editFlag = ref(false);
const newGroupFlag = ref(false);
const groupList = ref<{
  name: string;
  permissions: Array<object>;
}>([]);
const selectedGroup = ref({});

updateGroupList();

async function updateGroupList() {
  await $fetch(config.public.apiPath + "/groups/details", {
    retry: 0,
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
    onRequestError() {
      requestErrorAlert();
    },
    onResponse({ response }) {
      if (response.ok) {
        groupList.value = response._data;
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });
}

function resetSelectedGroup() {
  selectedGroup.value = {
    name: "",
    permissions: [],
  };
}

function addGroup() {
  resetSelectedGroup();
  editFlag.value = true;
  newGroupFlag.value = true;
}

function editGroup(group: object) {
  selectedGroup.value = group;
  editFlag.value = true;
  newGroupFlag.value = false;
}

async function deleteGroup(groupName: string) {
  if (
    !confirm("Are you sure you want to delete the group: " + groupName + "?")
  ) {
    return;
  }

  await $fetch(config.public.apiPath + "/group/" + groupName, {
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
        updateGroupList();
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedGroup();
  }
}

async function saveGroup(group: object) {
  try {
    if (newGroupFlag.value) {
      await $fetch(config.public.apiPath + "/group", {
        retry: 0,
        method: "POST",
        headers: {
          Authorization: "Bearer " + token.value,
        },
        body: group,
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          if (response.ok) {
            updateGroupList();
          }
        },
        onResponseError({ response }) {
          handleHttpError(response.status, response._data.error_description);
        },
      });
    } else {
      await $fetch(config.public.apiPath + "/group", {
        retry: 0,
        method: "PUT",
        headers: {
          Authorization: "Bearer " + token.value,
        },
        body: group,
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          if (response.ok) {
            updateGroupList();
          }
        },
        onResponseError({ response }) {
          handleHttpError(response.status, response._data.error_description);
        },
      });
    }
  } catch {
    console.log("Error in submit.")
    return;
  }
  alert("Group has been saved successfully.");
  resetSelectedGroup();
  editFlag.value = false;
}
</script>
