<template>
  <NuxtLayout name="base-layout">
    <title>Report Evolution</title>
    <template #page-title>Artifact Store</template>

    <div class="multi-line-checkbox-div" style="width: 100%">
      <label class="usa-label">Versions</label>
      <span
        v-for="(versionOption, index) in versionOptions"
        :key="index"
        class="multiple-per-line-checkbox"
        style="width: 30%"
      >
        <UsaCheckbox
          v-model="versionOption.selected"
          @update:model-value="
            versionChange(versionOption.selected, versionOption.name)
          "
        >
          {{ versionOption.name }}
        </UsaCheckbox>
      </span>
    </div>

    <div v-if="versionList.length === 0">No versions in model.</div>
    <div v-else>
      <UsaTable
        :headers="tableHeaders"
        :rows="filteredTableRows"
        borderless
        class="table"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;

const reports = ref<Dictionary<Array<ArtifactModel<ReportModel>>>>({});
const versionOptions = ref<Array<CheckboxOption>>([]);
const versionList = await getModelVersions(queryModel as string);
const tableHeaders = ref([
  { id: "version", label: "Version", sortable: true },
  { id: "identifier", label: "Identifier", sortable: true },
]);
const allTableRows = ref<Array<Dictionary<string>>>([]);
const filteredTableRows = ref<Array<Dictionary<string>>>([]);

if (versionList.length > 0) {
  // Populate versionOptions
  versionList.forEach((version: string) => {
    versionOptions.value.push(new CheckboxOption(version, true));
  });

  // Populate reports dict
  for (const version of versionList) {
    reports.value[version] = [];
    const artifacts = await getVersionArtifacts(queryModel as string, version);
    artifacts.forEach((artifact: ArtifactModel) => {
      if (artifact.body.artifact_type === "report") {
        reports.value[version].push(artifact as ArtifactModel<ReportModel>);
      }
    });
  }

  // TOOD: This isn't the best check, if the first version doesn't have a report, but later ones do this will break
  // TODO: Also needs to in some way account for the test case names changing, as this just takes the one from the first
  if (reports.value[versionList[0]].length > 0) {
    // Populate table headers
    Object.keys(
      reports.value[versionList[0]][0].body.test_results.results,
    ).forEach((key) => {
      tableHeaders.value.push({ id: key, label: key, sortable: false });
    });

    // Populate table rows
    versionList.forEach((version: string) => {
      reports.value[version].forEach((report) => {
        const row: Dictionary<string> = {
          version: version,
          identifier: report.header.identifier,
        };
        tableHeaders.value.forEach((header) => {
          if (header.id !== "version" && header.id !== "identifier") {
            row[header.id] = report.body.test_results.results[header.id].type;
          }
        });
        allTableRows.value.push(row);
      });
    });
  }

  filteredTableRows.value = allTableRows.value;
}

/**
 * Handle a version change either adding the version reports to table, or removing them
 *
 * @param {boolean} selected Flag indicating if verison was selected or deselected
 * @param {string} version String of the version name
 */
function versionChange(selected: boolean, version: string) {
  if (selected) {
    allTableRows.value.forEach((row: Dictionary<string>) => {
      if (row.version == version) {
        filteredTableRows.value.push(row);
      }
    });
    filteredTableRows.value.sort((a, b) => {
      if (a.version < b.version) {
        return -1;
      } else if (a.version > b.version) {
        return 1;
      } else {
        return 0;
      }
    });
  } else {
    filteredTableRows.value = filteredTableRows.value.filter(
      (item) => item.version !== version,
    );
  }
}
</script>
