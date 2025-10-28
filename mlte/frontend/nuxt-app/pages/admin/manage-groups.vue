<template>
  <NuxtLayout name="base-layout" @nav="handleNav">
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
        @delete-group="pageDeleteGroup"
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
const editFlag = ref(false);
const newGroupFlag = ref(false);
const groupList = ref<Array<Group>>([]);
const selectedGroup = ref<Group>(new Group());

updateGroupList();

// Get list of Groups from API and populate page with them.
async function updateGroupList() {
  groupList.value = await getGroupList();
}

// Reset selectedGroup, for example after an edit is completed.
function resetSelectedGroup() {
  selectedGroup.value = new Group();
}

// Switch to the edit group view with the newGroupFlag enabled.
function addGroup() {
  resetSelectedGroup();
  editFlag.value = true;
  newGroupFlag.value = true;
}

// Switch to the edit group view with the newGroupFlag disabled
function editGroup(group: Group) {
  selectedGroup.value = group;
  editFlag.value = true;
  newGroupFlag.value = false;
}

/**
 * Delete a group.
 *
 * @param {string} groupName Name of group to be deleted
 */
async function pageDeleteGroup(groupName: string) {
  if (
    !confirm("Are you sure you want to delete the group: " + groupName + "?")
  ) {
    return;
  }

  const response = await deleteGroup(groupName);
  if (response) {
    updateGroupList();
  }
}

// Handle navigation on sidebar, if editing it exits edit view
function handleNav() {
  if (editFlag.value) {
    cancelEdit();
  }
}

// Return to the group list view from the edit view.
function cancelEdit() {
  if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
    editFlag.value = false;
    resetSelectedGroup();
  }
}

/**
 * Save new Group, or save changes to Group.
 *
 * @param {Group} group Group to be saved
 */
async function saveGroup(group: Group) {
  let error = true;

  if (newGroupFlag.value) {
    const response = await createGroup(group);
    if (response) {
      error = false;
    }
  } else {
    const response = await updateGroup(group);
    if (response) {
      error = false;
    }
  }

  if (!error) {
    updateGroupList();
    resetSelectedGroup();
    editFlag.value = false;
  }
}
</script>
