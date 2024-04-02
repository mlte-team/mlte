<template>
  <NuxtLayout name="base-layout">
    <table class="table usa-table usa-table--borderless">
      <thead>
        <tr>
          <th data-sortable scope="col" role="columnheader">Username</th>
          <th data-sortable scope="col" role="columnheader">Email</th>
          <th data-sortable scope="col" role="columnheader">Full Name</th>
          <th data-sortable scope="col" role="columnheader">Disabled</th>
          <th scope="col" role="columnheader">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in userList" :key="index">
          <td v-if="!user.edit" class="input-box">
            {{ user.username }}
          </td>
          <td v-else>
            <UsaTextInput v-model="user.username" class="input-box" />
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
          <td>
            <UsaButton
              v-if="!user.edit"
              class="secondary-button"
              @click="enableEdit(user)"
            >
              Edit
            </UsaButton>
            <UsaButton
              v-if="user.edit"
              class="secondary-button"
              @click="saveEdit(user)"
            >
              Save
            </UsaButton>
            <UsaButton class="usa-button usa-button--secondary">
              Delete
            </UsaButton>
          </td>
        </tr>
      </tbody>
    </table>
    <UsaButton class="primary-button" @click="addUser()"> Add User </UsaButton>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const userList = ref<
  {
    username: string;
    email: string;
    full_name: string;
    disabled: boolean;
    password: string;
    edit: boolean;
  }[]
>([]);

await useFetch(config.public.apiPath + "/users/details", {
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
  },
  onResponseError() {
    responseErrorAlert();
  },
});

function addUser() {
  userList.value.push({
    username: "",
    email: "",
    full_name: "",
    disabled: false,
    password: "",
    edit: true,
  });
}

function enableEdit(user: any) {
  user.edit = true;
}

function saveEdit(user: any) {
  // TODO : Post to backend

  user.edit = false;
}

function deleteUser(username: string) {}
</script>

<style>
.input-box {
  max-width: 10rem;
}
</style>
