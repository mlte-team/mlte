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
const userCookie = useCookie("user");

const editFlag = ref(false);
const newUserFlag = ref(false);
const userList = ref<Array<User>>([]);
const selectedUser = ref<User>(new User());

updateUserList();
resetSelectedUser();

/**
 * 
 */
async function updateUserList() {
  const data: Array<User> | null = await useApi("/users/details", "GET");
  if (data) {
    userList.value = data;
  }
}

/**
 * 
 */
function resetSelectedUser() {
  selectedUser.value = new User();
}

/**
 * 
 */
function addUser() {
  resetSelectedUser();
  editFlag.value = true;
  newUserFlag.value = true;
}

/**
 * 
 */
function editUser(user: User) {
  selectedUser.value = user;
  editFlag.value = true;
  newUserFlag.value = false;
}

/**
 * 
 * @param username 
 */
async function deleteUser(username: string) {
  if (userCookie.value === username) {
    alert("Cannot delete the active user.");
    return;
  }
  if (!confirm("Are you sure you want to delete user, " + username + "?")) {
    return;
  }

  const data = await useApi("/user/" + username, "DELETE");
  if (data) {
    updateUserList();
  }
}

/**
 * 
 */
function manageUserClick() {
  if (editFlag.value) {
    cancelEdit();
  }
}

/**
 * 
 */
function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedUser();
  }
}

/**
 * 
 * @param user 
 */
async function saveUser(user: User) {
  let error = true;

  if (newUserFlag.value) {
    const data = await useApi("/user", "POST", {
      body: JSON.stringify(user),
    });
    if (data) {
      error = false;
    }
  } else {
    const data = await useApi("/user", "PUT");
    if (data) {
      error = false;
    }
  }

  if (!error) {
    updateUserList();
    resetSelectedUser();
    editFlag.value = false;
    successfulSubmission("User", user.username, "saved");
  }
}
</script>
