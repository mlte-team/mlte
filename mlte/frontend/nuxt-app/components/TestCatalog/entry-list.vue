<template>
  <table class="table usa-table usa-table--borderless">
    <thead>
      <tr>
        <th data-sortable scope="col" role="columnheader">Identifier</th>
        <th data-sortable scope="col" role="columnheader">Actions</th>
      </tr>
    </thead>
    <tr v-for="(entry, entryIndex) in modelValue" :key="entryIndex">
      <td>
        {{ entry.header.identifier }}
      </td>
      <td>
        <UsaButton class="secondary-button" @click="$emit('editEntry', entry)">
          Edit
        </UsaButton>
        <UsaButton
          class="usa-button usa-button--secondary"
          @click="$emit('deleteEntry', entry.header.identifier)"
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
    type: Array,
    required: true,
    default: [],
  },
});
</script>
