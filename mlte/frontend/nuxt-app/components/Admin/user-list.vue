<template>
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
      <tr v-for="(user, index) in modelValue" :key="index">
        <td>
          {{ user.username }}
        </td>
        <td>
          {{ user.email }}
        </td>
        <td>
          {{ user.full_name }}
        </td>
        <td>
          <div class="centered-container" style="margin-bottom: 1.5em">
            <UsaCheckbox v-model="user.disabled" disabled />
          </div>
        </td>
        <td>
          <UsaButton
            class="secondary-button"
            @click="$emit('editUser', user)"
          >
            Edit
          </UsaButton>

          <UsaButton
            class="usa-button usa-button--secondary"
            @click="$emit('deleteUser', user.username)"
          >
            Delete
          </UsaButton>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
const emit = defineEmits([
  "addUser",
  "editUser",
  "deleteUser"
])

const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: []
  }
})
</script>