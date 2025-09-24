<template>
  <table class="table usa-table usa-table--borderless">
    <thead>
      <tr>
        <th scope="col" role="columnheader">Name</th>
        <th scope="col" role="columnheader">Description</th>
        <th scope="col" role="columnheader">Parent</th>
        <th scope="col" role="columnheader">Actions</th>
      </tr>
    </thead>
    <tr v-for="(entry, entryIndex) in modelValue" :key="entryIndex">
      <td>{{ entry.name }}</td>
      <td>{{ entry.description }}</td>
      <td>{{ entry.parent }}</td>
      <td>
        <UsaButton class="secondary-button" @click="emit('editEntry', entry)">
          Edit
        </UsaButton>
        <UsaButton
          class="usa-button usa-button--secondary"
          @click="emit('deleteEntry', entry.name)"
        >
          Delete
        </UsaButton>
      </td>
    </tr>
  </table>
</template>

<script setup lang="ts">
const emit = defineEmits(["addEntry", "editEntry", "deleteEntry"]);
const props = defineProps({
  modelValue: {
    type: Array<CustomListEntry>,
    required: true,
  },
});
</script>
