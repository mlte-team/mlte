<template>
  <NuxtLayout name="base-layout">
    <title>Report Evolution</title>
    <template #page-title>Artifact Store</template>
    <div v-if="versions.length === 0">No versions in model.</div>
    <div v-else>
      <UsaTable
        :headers="tableHeaders"
        :rows="tableRows"
        borderless
        class="table"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;

const reports = ref<Dictionary<Array<ArtifactModel<ReportModel>>>>({});
const versions = await getModelVersions(queryModel as string);
const tableHeaders = ref([
  { id: "version", label: "Version", sortable: false },
]);
const tableRows = ref<Array<Dictionary<string>>>([]);

if (versions.length > 0) {
  // Populate reports dict
  for (const version of versions) {
    reports.value[version] = [];
    const artifacts = await getVersionArtifacts(queryModel as string, version);
    artifacts.forEach((artifact: ArtifactModel) => {
      if (artifact.body.artifact_type === "report") {
        reports.value[version].push(artifact as ArtifactModel<ReportModel>);
      }
    });
  }

  // TOOD: This isn't the best check, if the first version doesn't have a report, but later ones do this will breka
  // TODO: Also needs to in some way account for the test case names changing, as this just takes the one from the first
  if (reports.value[versions[0]].length > 0) {
    // Populate table headers
    Object.keys(
      reports.value[versions[0]][0].body.test_results.results,
    ).forEach((key) => {
      tableHeaders.value.push({ id: key, label: key, sortable: false });
    });

    // Populate table rows
    versions.forEach((version: string) => {
      reports.value[version].forEach((report) => {
        const row: Dictionary<string> = {
          version: version,
        };
        tableHeaders.value.forEach((header) => {
          if (header.id !== "version") {
            row[header.id] = report.body.test_results.results[header.id].type;
          }
        });
        tableRows.value.push(row);
      });
    });
  }
}
</script>
