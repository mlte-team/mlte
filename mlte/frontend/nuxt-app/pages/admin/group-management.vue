<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 100px">
        <UsaTextInput
          v-model="newGroupName"
        >
          <template #label>
            New Group
          </template>
        </UsaTextInput>
        <UsaButton
          class="secondary-button margin-button"
          @click="addGroup"
        >
          Add Group
        </UsaButton>
      </div>
    </template>

    <table class="table usa-table usa-table--borderless">
      <thead>
        <tr>
          <th data-sortable scope="col" role="columnheader">Name</th>
          <th data-sortable scope="col" role="columnheader">Permissions <br/> (Resource Type - Resource ID - Method)</th>
          <th data-sortable scope="col" role="columnheader">Actions</th>
        </tr>
      </thead>
      <tr v-for="(group, groupIndex) in groupList" :key="groupIndex">
        <td>
          {{ group.name }}
        </td>
        <td>
          <div v-for="(permission, permissionIndex) in group.permissions" :key="permissionIndex">
            <span v-if="permission.resource_id === null">
              {{ permission.resource_type }} - (All) - {{ permission.method }}
            </span>
            <span v-else>
              {{ permission.resource_type }} - {{ permission.resource_id }} - {{ permission.method }}
            </span>
          </div>
        </td>
        <td>
          <UsaButton
            class="secondary-button"
          >
            Edit
          </UsaButton>
          <UsaButton
            class="usa-button usa-button--secondary"
          >
            Delete
          </UsaButton>
        </td>
      </tr>
    </table>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const newGroupName = ref("");
const groupList = ref<
  {
    name: string,
    permissions: Array<object>,
  }
>([]);

updateGroupList();

async function updateGroupList(){
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

function addGroup(){
  if(newGroupName.value.trim() === ""){
    return;
  }
  
  console.log("Unimplemented")
}
</script>