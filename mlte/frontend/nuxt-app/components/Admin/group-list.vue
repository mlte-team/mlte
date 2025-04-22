<template>
  <table class="table usa-table usa-table--borderless">
    <thead>
      <tr>
        <th data-sortable scope="col" role="columnheader">Name</th>
        <th data-sortable scope="col" role="columnheader">
          Permissions <br />
          (Resource Type - Resource ID - Method)
        </th>
        <th data-sortable scope="col" role="columnheader">Actions</th>
      </tr>
    </thead>
    <tr v-for="(group, groupIndex) in props.modelValue" :key="groupIndex">
      <td>
        {{ group.name }}
      </td>
      <td>
        <div
          v-for="(permission, permissionIndex) in group.permissions"
          :key="permissionIndex"
        >
          <div class="inline-input-left" style="max-width: 50ch">
            <span v-if="permission.resource_id === null">
              {{ permission.resource_type }} - (All) - {{ permission.method }}
            </span>
            <span v-else>
              {{ permission.resource_type }} - {{ permission.resource_id }} -
              {{ permission.method }}
            </span>
          </div>
        </div>
      </td>
      <td>
        <UsaButton class="secondary-button" @click="$emit('editGroup', group)">
          Edit
        </UsaButton>
        <UsaButton
          class="usa-button usa-button--secondary"
          @click="$emit('deleteGroup', group.name)"
        >
          Delete
        </UsaButton>
      </td>
    </tr>
  </table>
</template>

<script setup lang="ts">
const emits = defineEmits(["addGroup", "editGroup", "deleteGroup"]);
const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: [],
  },
});
</script>
