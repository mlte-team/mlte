<template>
  <NuxtLayout name="base-layout">
    <table class="table usa-table usa-table--borderless">
      <thead>
        <tr>
          <th data-sortable scope="col" role="columnheader">Username</th>
          <th data-sortable scope="col" role="columnheader">Email</th>
          <th data-sortable scope="col" role="columnheader">Full Name</th>
          <th data-sortable scope="col" role="columnheader">Disabled</th>
          <th data-sortable scope="col" role="columnheader">Password</th>
          <th scope="col" role="columnheader">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in userList" :key="index">
          <td v-if="!user.newUser">
            {{ user.username }}
          </td>
          <td v-else>
            <UsaTextInput
              v-model="user.username"
              type="email"
              class="input-box"
            />
          </td>
          <td v-if="!user.edit">
            {{ user.email }}
          </td>
          <td v-else>
            <UsaTextInput v-model="user.email" class="input-box" />
          </td>
          <td v-if="!user.edit">
            {{ user.full_name }}
          </td>
          <td v-else>
            <UsaTextInput v-model="user.full_name" class="input-box" />
          </td>
          <td v-if="!user.edit">
            <div class="centered-container" style="margin-bottom: 1.5em">
              <UsaCheckbox v-model="user.disabled" disabled />
            </div>
          </td>
          <td v-else>
            <div class="centered-container" style="margin-bottom: 1.5em">
              <UsaCheckbox v-model="user.disabled" />
            </div>
          </td>
          <td v-if="!user.newUser">*****</td>
          <td v-else>
            <UsaTextInput v-model="user.password" class="input-box" />
          </td>
          <td v-if="!user.edit">
            <UsaButton class="secondary-button" @click="editUser(user)">
              Edit
            </UsaButton>

            <UsaButton
              class="usa-button usa-button--secondary"
              @click="deleteUser(user.username)"
            >
              Delete
            </UsaButton>
          </td>
          <td v-else>
            <UsaButton class="secondary-button" @click="cancelEdit(user)">
              Cancel
            </UsaButton>
            <UsaButton
              v-if="user.edit"
              class="secondary-button"
              @click="saveUser(user)"
            >
              Save
            </UsaButton>
          </td>
        </tr>
      </tbody>
    </table>
    <UsaButton
      v-if="addUserButtonFlag"
      class="primary-button"
      @click="addUser()"
    >
      Add User
    </UsaButton>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const user = useCookie("user");

const addUserButtonFlag = ref(true);
const userList = ref<
  {
    username: string;
    email: string;
    full_name: string;
    disabled: boolean;
    password: string;
    edit: boolean;
    newUser: boolean;
  }[]
>([]);

updateUserList();

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
      userList.value.forEach((user) => (user.edit = false));
      userList.value.forEach((user) => (user.newUser = false));
    },
    onResponseError() {
      responseErrorAlert();
    },
  });
}

function editUser(user: any) {
  user.edit = true;
}

function cancelEdit(user: any) {
  if (user.newUser) {
    userList.value.pop();
    addUserButtonFlag.value = true;
  } else {
    user.edit = false;
  }
}

function addUser() {
  userList.value.push({
    username: "",
    email: "",
    full_name: "",
    disabled: false,
    password: "",
    edit: true,
    newUser: true,
  });

  addUserButtonFlag.value = false;
}

async function saveUser(user: any) {
  if (user.newUser) {
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

    addUserButtonFlag.value = true;
  } else {
    await $fetch(config.public.apiPath + "/user", {
      retry: 0,
      method: "PUT",
      body: {
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        disabled: user.disabled,
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

  user.edit = false;
}

async function deleteUser(username: string) {
  if (username === user.value) {
    alert("Cannot delete the active user.");
  } else if (
    confirm("Are you sure you want to delete user, " + username + "?")
  ) {
    await $fetch(config.public.apiPath + "/user/" + username, {
      retry: 0,
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        console.log("deleted");
        updateUserList();
      },
      onResponseError() {
        responseErrorAlert();
      },
    });
  }
}
</script>

<style>
.input-box {
  max-width: 7rem;
}
</style>
