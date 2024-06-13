<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 80px">
        <UsaButton class="secondary-button margin-button" @click="addGroup">
          Add Group
        </UsaButton>
      </div>
    </template>

    <div v-if="!editFlag">
      <AdminGroupList
        v-model="groupList"
        @editGroup="editGroup"
        @deleteGroup="deleteGroup"
      />
    </div>
    <div v-if="editFlag">
      <AdminEditGroup
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
      groupList.value = response._data;
    },
    onResponseError() {
      responseErrorAlert();
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
    onResponse() {
      updateGroupList();
    },
    onResponseError() {
      responseErrorAlert();
    },
  });
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedGroup();
  }
}

// async function saveGroup(group: object) {
//   if (newGroupFlag.value) {
//     if (user.username === "" || user.password === "") {
//       alert("Username and password are required.");
//       return;
//     }

//     await $fetch(config.public.apiPath + "/user", {
//       retry: 0,
//       method: "POST",
//       headers: {
//         Authorization: "Bearer " + token.value,
//       },
//       body: {
//         username: user.username,
//         email: user.email,
//         full_name: user.full_name,
//         disabled: user.disabled,
//         role: user.role,
//         groups: user.groups,
//         password: user.password,
//       },
//       onRequestError() {
//         requestErrorAlert();
//       },
//       onResponse({ response }) {
//         updateUserList();
//       },
//       onResponseError() {
//         responseErrorAlert();
//       },
//     });
//   } else {
//     await $fetch(config.public.apiPath + "/user", {
//       retry: 0,
//       method: "PUT",
//       body: {
//         username: user.username,
//         email: user.email,
//         full_name: user.full_name,
//         disabled: user.disabled,
//         role: user.role,
//         groups: user.groups,
//         password: user.password,
//       },
//       headers: {
//         Authorization: "Bearer " + token.value,
//       },
//       onRequestError() {
//         requestErrorAlert();
//       },
//       onResponse({ response }) {
//         updateUserList();
//       },
//       onResponseError() {
//         responseErrorAlert();
//       },
//     });
//   }

//   resetSelectedUser();
//   editFlag.value = false;
// }
</script>
