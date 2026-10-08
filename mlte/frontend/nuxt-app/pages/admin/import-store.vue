<template>
  <NuxtLayout name="base-layout">
    <title>Import Store</title>
    <template #page-title>Import Store</template>
    <div>
      <UsaCheckbox v-model="forceImport">
        Overwrite data with import
      </UsaCheckbox>

      <div
        v-if="forceImport"
        class="usa-alert usa-alert--warning margin-bottom-2"
      >
        <div class="usa-alert__body">
          <p class="usa-alert__text">
            Importing data will overwrite your current configuration.
          </p>
        </div>
      </div>

      <UsaFileInput accept=".json" @change="handleImportFile">
        <template #label>Select a JSON file to import.</template>
      </UsaFileInput>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const forceImport = ref(false);

async function handleImportFile(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0 && target.files[0]) {
    await importStore(target.files[0], forceImport.value);
  }

  window.location.href = "/";
}
</script>
