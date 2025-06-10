<template>
  <NuxtLayout name="base-layout" @manage-users="manageUserClick">
    <title>Manage Users</title>
    <template #page-title>Manage Users</template>
    <div v-if="!editFlag">
      <UsaButton
        class="secondary-button sub-header-float-button"
        @click="addUser"
      >
        Add User
      </UsaButton>
      <AdminUserList
        v-model="userList"
        @edit-user="editUser"
        @delete-user="deleteUser"
      />
    </div>
    <div v-if="editFlag">
      <AdminUserEdit
        v-model="selectedUser"
        :new-user-flag="newUserFlag"
        @cancel="cancelEdit"
        @submit="saveUser"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const userCookie = useCookie("user");

const editFlag = ref(false);
const newUserFlag = ref(false);
const userList = ref<Array<User>>([]);
const selectedUser = ref({});

updateUserList();
resetSelectedUser();

async function updateUserList() {
  await $fetch(config.public.apiPath + "/users/details", {
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
        userList.value = response._data;
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });
}

function resetSelectedUser() {
  selectedUser.value = new User();
}

function addUser() {
  resetSelectedUser();
  editFlag.value = true;
  newUserFlag.value = true;
}

function editUser(user: object) {
  selectedUser.value = user;
  editFlag.value = true;
  newUserFlag.value = false;
}

async function deleteUser(usernameToDelete: string) {
  if (userCookie.value === usernameToDelete) {
    alert("Cannot delete the active user.");
    return;
  }
  if (
    !confirm("Are you sure you want to delete user, " + usernameToDelete + "?")
  ) {
    return;
  }

  await $fetch(config.public.apiPath + "/user/" + usernameToDelete, {
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
        updateUserList();
      }
    },
    onResponseError({ response }) {
      handleHttpError(response.status, response._data.error_description);
    },
  });
}

function manageUserClick() {
  if (editFlag.value) {
    cancelEdit();
  }
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedUser();
  }
}

async function saveUser(user: object) {
  try {
    if (newUserFlag.value) {
      await $fetch(config.public.apiPath + "/user", {
        retry: 0,
        method: "POST",
        headers: {
          Authorization: "Bearer " + token.value,
        },
        body: user,
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          if (response.ok) {
            updateUserList();
          }
        },
        onResponseError({ response }) {
          handleHttpError(response.status, response._data.error_description);
        },
      });
    } else {
      await $fetch(config.public.apiPath + "/user", {
        retry: 0,
        method: "PUT",
        body: user,
        headers: {
          Authorization: "Bearer " + token.value,
        },
        onRequestError() {
          requestErrorAlert();
        },
        onResponse({ response }) {
          if (response.ok) {
            updateUserList();
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
  alert("User has been saved successfully.");
  resetSelectedUser();
  editFlag.value = false;
}
</script>
