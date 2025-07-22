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
const editFlag = ref(false);
const newGroupFlag = ref(false);
const groupList = ref<Array<Group>>([]);
const selectedGroup = ref<Group>(new Group());

updateGroupList();

// Get list of Groups from API and populate page with them.
async function updateGroupList() {
  const data: Array<Group> | null = await useApi("/groups/details", "GET");
  if (data) {
    groupList.value = [];
    data.forEach((group: Group) => {
      groupList.value.push(group);
    });
  }
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
async function deleteGroup(groupName: string) {
  if (
    !confirm("Are you sure you want to delete the group: " + groupName + "?")
  ) {
    return;
  }

  const data = await useApi("/group/" + groupName, "DELETE");
  if (data) {
    updateGroupList();
    successfulSubmission("Group", groupName, "deleted");
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
    const data = await useApi("/group", "POST", {
      body: JSON.stringify(group),
    });
    if (data) {
      error = false;
    }
  } else {
    const data = await useApi("/group", "PUT", {
      body: JSON.stringify(group),
    });
    if (data) {
      error = false;
    }
  }

  if (!error) {
    updateGroupList();
    resetSelectedGroup();
    editFlag.value = false;
    successfulSubmission("Group", group.name, "saved");
  }
}
</script>
