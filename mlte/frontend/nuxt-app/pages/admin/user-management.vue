<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 80px">
        <div v-if="!editFlag">
          <UsaButton class="secondary-button" @click="addUser">
            Add User
          </UsaButton>
        </div>
      </div>
    </template>

    <div v-if="!editFlag">
      <AdminUserList
        v-model="userList"
        @editUser="editUser"
        @deleteUser="deleteUser"
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
const authUser = useCookie("user");

const editFlag = ref(false);
const newUserFlag = ref(false);
const userList = ref<
  {
    username: string;
    email: string;
    full_name: string;
    disabled: boolean;
    role: string;
    groups: Array<object>;
    password: string;
  }[]
>([]);
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
      userList.value = response._data;
    },
    onResponseError() {
      responseErrorAlert();
    },
  });
}

function resetSelectedUser() {
  selectedUser.value = {
    username: "",
    email: "",
    full_name: "",
    disabled: false,
    role: "",
    groups: [],
    password: "",
  };
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
  if (authUser.value === usernameToDelete) {
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
    onResponse() {
      updateUserList();
    },
    onResponseError() {
      responseErrorAlert();
    },
  });
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedUser();
  }
}

async function saveUser(user: object) {
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
      onResponse() {
        updateUserList();
      },
      onResponseError() {
        responseErrorAlert();
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
      onResponse() {
        updateUserList();
      },
      onResponseError() {
        responseErrorAlert();
      },
    });
  }

  resetSelectedUser();
  editFlag.value = false;
}
</script>
