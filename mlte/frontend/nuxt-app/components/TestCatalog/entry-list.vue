<template>
  <table class="table usa-table usa-table--borderless">
    <thead>
      <tr>
        <th data-sortable scope="col" role="columnheader">Identifier</th>
        <th data-sortable scope="col" role="columnheader">Catalog</th>
        <th data-sortable scope="col" role="columnheader">Tags</th>
        <th data-sortable scope="col" role="columnheader">Property Category</th>
        <th data-sortable scope="col" role="columnheader">Code Type</th>
        <th data-sortable scope="col" role="columnheader">Actions</th>
      </tr>
    </thead>
    <tr v-for="(entry, entryIndex) in modelValue" :key="entryIndex">
      <td>
        {{ entry.header.identifier }}
      </td>
      <td>
        {{ entry.header.catalog_id }}
      </td>
      <td>
        <span v-for="(tag, tagIndex) in entry.problem_type">
          <span>{{ tag }}</span>
          <span v-if="tagIndex + 1 < entry.problem_type.length">, </span>
        </span>
      </td>
      <td>
        {{ entry.property_category }}
      </td>
      <td>
        {{ entry.code_type }}
      </td>
      <td style="width: 13em">
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
