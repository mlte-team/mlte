<template>
  <NuxtLayout name="base-layout">
    <div v-if="!editFlag">
      <AdminUserManagementUserList 
        v-model="userList"
        @addUser="addUser"
        @editUser="editUser"
        @deleteUser="deleteUser"
      />
    </div>
    <div v-if="editFlag">
      <AdminUserManagementEditUser
        v-model="selectedUser"
        :newUserFlag="newUserFlag"
        @cancel="cancelEdit"
        @submit="saveUser"
        @updateUserGroups="updateUserGroups"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const authUser = useCookie("user")

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

function resetSelectedUser(){
  selectedUser.value = {
    username: "",
    email: "",
    full_name: "",
    disabled: false,
    role: "",
    groups: [],
    password: "",
  }
}

function addUser(){
  resetSelectedUser();
  editFlag.value = true;
  newUserFlag.value = true;
}

function editUser(user: any){
  selectedUser.value = user;
  editFlag.value = true;
  newUserFlag.value = false;
}

async function deleteUser(usernameToDelete: string){
  console.log(authUser.value);
  console.log(usernameToDelete)

  if (authUser.value === usernameToDelete) {
    alert("Cannot delete the active user.");
  } else if (
    confirm("Are you sure you want to delete user, " + usernameToDelete + "?")
  ) {
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
        updateUserList();
      },
      onResponseError() {
        responseErrorAlert();
      },
    });
  }
}

function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")){
    editFlag.value = false;
    resetSelectedUser();
  }
}

function updateUserGroups(groupList: Array<object>){
  selectedUser.value.groups = groupList;
}

async function saveUser(user: any) {
  if (newUserFlag.value) {
    if (user.username === "" || user.password === "") {
      alert("Username and password are required.");
      return;
    }

    await $fetch(config.public.apiPath + "/user", {
      retry: 0,
      method: "POST",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: {
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        disabled: user.disabled,
        role: user.role,
        groups: user.groups,
        password: user.password,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
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
      body: {
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        disabled: user.disabled,
        role: user.role,
        groups: user.groups,
        password: user.password,
      },
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
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

<style>
.input-box {
  max-width: 7rem;
}
</style>
