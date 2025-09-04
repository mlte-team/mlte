<template>
  <NuxtLayout name="base-layout">
    <title>Report Evolution</title>
    <template #page-title>Artifact Store</template>

    <div v-if="versionList.length === 0">No versions in model.</div>
    <div v-else-if="firstReportIndex === -1">
      No reports in any model versions.
    </div>
    <div v-else>
      <div
        class="multi-line-checkbox-div"
        style="width: 100%; display: inline-block"
      >
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

      <div style="overflow-x: scroll">
        <table class="table usa-table usa-table--borderless sortable">
          <thead>
            <tr data-sort-method="none">
              <th
                v-for="(header, index) in tableHeaders"
                :key="index"
                data-sortable
                scope="col"
                role="columnheader"
              >
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in filteredTableRows" :key="index">
              <template v-for="(value, key) in row" :key="key">
                <td v-if="key === 'identifier'">
                  <NuxtLink
                    :to="{
                      path: '/artifact-views/report-view',
                      query: {
                        model: queryModel,
                        version: row.version,
                        artifactId: row.identifier,
                      },
                    }"
                    target="_blank"
                  >
                    {{ value.value }}
                  </NuxtLink>
                </td>
                <td v-else-if="value.value === 'Success'" class="success-td">
                  <span class="tooltip">
                    {{ value.value }}
                    <span class="tooltiptext">
                      {{ value.value }}: {{ value.message }}
                    </span>
                  </span>
                </td>
                <td v-else-if="value.value === 'Info'" class="info-td">
                  <span class="tooltip">
                    {{ value.value }}
                    <span class="tooltiptext">
                      {{ value.value }}: {{ value.message }}
                    </span>
                  </span>
                </td>
                <td v-else-if="value.value === 'Failure'" class="failure-td">
                  <span class="tooltip">
                    {{ value.value }}
                    <span class="tooltiptext">
                      {{ value.value }}: {{ value.message }}
                    </span>
                  </span>
                </td>
                <td v-else>
                  {{ value.value }}
                </td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;

const reports = ref<Dictionary<Array<ArtifactModel<ReportModel>>>>({});
const versionOptions = ref<Array<CheckboxOption>>([]);
const versionList = await getModelVersions(queryModel as string);
const tableHeaders = ref<Array<string>>(["Version", "Identifier"]);
const allTableRows = ref<Array<Dictionary<Dictionary<string>>>>([]);
const filteredTableRows = ref<Array<Dictionary<Dictionary<string>>>>([]);

const firstReportIndex = ref(-1);

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

  firstReportIndex.value = Object.keys(reports.value).findIndex(
    (version: string) => {
      return reports.value[version].length > 0;
    },
  );
  if (firstReportIndex.value > -1) {
    // Populate table headers with all test result id's from any report
    Object.keys(reports.value).forEach((reportKey: string) => {
      reports.value[reportKey].forEach((report: ArtifactModel<ReportModel>) => {
        Object.keys(report.body.test_results.results).forEach(
          (test_result_id: string) => {
            if (!tableHeaders.value.includes(test_result_id)) {
              tableHeaders.value.push(test_result_id);
            }
          },
        );
      });
    });

    // Populate table rows
    versionList.forEach((version: string) => {
      reports.value[version].forEach((report) => {
        const row: Dictionary<Dictionary<string>> = {
          version: { value: version },
          identifier: { value: report.header.identifier },
        };
        tableHeaders.value.forEach((header) => {
          if (header !== "Version" && header !== "Identifier") {
            if (header in report.body.test_results.results) {
              row[header] = {
                value: report.body.test_results.results[header].type,
                message: report.body.test_results.results[header].message,
              };
            } else {
              row[header] = {
                value: "N/A",
                message: "N/A",
              };
            }
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
    allTableRows.value.forEach((row: Dictionary<Dictionary<string>>) => {
      if (row.version.value == version) {
        filteredTableRows.value.push(row);
      }
    });
    filteredTableRows.value.sort((a, b) => {
      if (a.version.value < b.version.value) {
        return -1;
      } else if (a.version.value > b.version.value) {
        return 1;
      } else {
        return 0;
      }
    });
  } else {
    filteredTableRows.value = filteredTableRows.value.filter(
      (item) => item.version.value !== version,
    );
  }
}
</script>
