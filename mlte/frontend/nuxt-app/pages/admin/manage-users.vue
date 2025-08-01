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

// Get list of Users form API and populate page with them.
async function updateUserList() {
  const users: Array<User> | null = await useApi("/users/details", "GET");
  if (users) {
    userList.value = users;
  }
}

// Reset selectedUser, for example after an edit is completed.
function resetSelectedUser() {
  selectedUser.value = new User();
}

// Switch to the edit user view with newUserFlag enabled.
function addUser() {
  resetSelectedUser();
  editFlag.value = true;
  newUserFlag.value = true;
}

// Switch to the edit user view with newUserFlag disbled.
function editUser(user: User) {
  selectedUser.value = user;
  editFlag.value = true;
  newUserFlag.value = false;
}

/**
 * Delete a user.
 *
 * @param {string} username Username of user to be deleted
 */
async function deleteUser(username: string) {
  if (userCookie.value === username) {
    alert("Cannot delete the active user.");
    return;
  }
  if (!confirm("Are you sure you want to delete user, " + username + "?")) {
    return;
  }

  const response = await useApi("/user/" + username, "DELETE");
  if (response) {
    updateUserList();
  }
}

// Intended to return to user list view when Manage Users in sidebar is clicked and edit view is enabled
// TODO : Fix this, currently doesn't work. Base layout doesn't seem to emit the event this listens for.
// TODO : Mirror this fixed functionality in Manage Groups
function manageUserClick() {
  if (editFlag.value) {
    cancelEdit();
  }
}

// Return to user list view from the edit view.
function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedUser();
  }
}

/**
 * Save new User, or save changes to User.
 *
 * @param {User} user User to be saved
 */
async function saveUser(user: User) {
  let error = true;

  if (newUserFlag.value) {
    const response = await useApi("/user", "POST", {
      body: JSON.stringify(user),
    });
    if (response) {
      error = false;
    }
  } else {
    const response = await useApi("/user", "PUT");
    if (response) {
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
