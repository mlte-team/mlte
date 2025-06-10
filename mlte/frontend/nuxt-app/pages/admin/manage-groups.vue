<template>
  <NuxtLayout name="base-layout">
    <title>Manage Groups</title>
    <template #page-title>Manage Groups</template>
    <div v-if="!editFlag">
      <UsaButton
        class="secondary-button sub-header-float-button"
        @click="addGroup"
      >
        Add Group
      </UsaButton>
      <AdminGroupList
        v-model="groupList"
        @edit-group="editGroup"
        @delete-group="deleteGroup"
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
const groupList = ref<Array<Group>>([]);
const selectedGroup = ref<Group>(new Group());

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
        response._data.forEach((group: Group) => {
          groupList.value.push(new Group(group.name, group.permissions));
        });
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });
}

function resetSelectedGroup() {
  selectedGroup.value = new Group();
}

function addGroup() {
  resetSelectedGroup();
  editFlag.value = true;
  newGroupFlag.value = true;
}

function editGroup(group: Group) {
  selectedGroup.value = group as Group;
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

async function saveGroup(group: Group) {
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
  } catch (exception) {
    console.log("Error in submit.");
    console.log(exception);
    return;
  }
  alert("Group has been saved successfully.");
  resetSelectedGroup();
  editFlag.value = false;
}
</script>
