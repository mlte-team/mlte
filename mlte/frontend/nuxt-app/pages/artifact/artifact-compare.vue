<template>
  <NuxtLayout name="base-layout">
    <title>Report Compare</title>
    <template #page-title>Report Compare</template>
    <h1 class="section-header">{{ queryModel }}</h1>

    <div class="row">
      <div class="column">
        <div class="half-line-input">
          <UsaSelect
            v-model="versionSelection1"
            :options="versionOptions"
            @update:model-value="selectVersion(1, $event)"
          >
            <template #label>Version 1 </template>
          </UsaSelect>
        </div>
        <div class="half-line-input">
          <UsaSelect
            v-model="reportSelection1"
            :options="reportOptions1"
            @update:model-value="selectReport(1, $event)"
          >
            <template #label>Report 1 </template>
          </UsaSelect>
        </div>
      </div>
      <div class="column">
        <div class="half-line-input">
          <UsaSelect
            v-model="versionSelection2"
            :options="versionOptions"
            @update:model-value="selectVersion(2, $event)"
          >
            <template #label> Version 2 </template>
          </UsaSelect>
        </div>
        <div class="half-line-input">
          <UsaSelect
            v-model="reportSelection2"
            :options="reportOptions2"
            @update:model-value="selectReport(2, $event)"
          >
            <template #label>Report 2 </template>
          </UsaSelect>
        </div>
      </div>
    </div>
    <div v-if="report1 && report2">
      <ReportCompare
        :version1="versionSelection1"
        :version2="versionSelection2"
        :report1="report1"
        :report2="report2"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;
const versionOptions = ref<Array<SelectOption>>([]);

const versionSelection1 = ref<string>("");
const reportList1 = ref<Array<ArtifactModel<ReportModel>>>([]);
const reportOptions1 = ref<Array<SelectOption>>([]);
const reportSelection1 = ref<string>("");
const report1 = ref<ArtifactModel<ReportModel>>();

const versionSelection2 = ref<string>("");
const reportList2 = ref<Array<ArtifactModel<ReportModel>>>([]);
const reportOptions2 = ref<Array<SelectOption>>([]);
const reportSelection2 = ref<string>("");
const report2 = ref<ArtifactModel<ReportModel>>();

const modelVersions = await getModelVersions(queryModel as string);
if (modelVersions) {
  modelVersions.forEach((version: string) => {
    versionOptions.value.push(new SelectOption(version, version));
  });
}

if (modelVersions.length > 1) {
  selectVersion(1, modelVersions[modelVersions.length - 2]);
  selectVersion(2, modelVersions[modelVersions.length - 1]);
} else if (modelVersions.length === 1) {
  selectVersion(1, modelVersions[modelVersions.length - 1]);
  selectVersion(2, modelVersions[modelVersions.length - 1]);
}

/**
 * Handle selection of a new Version. Loads new Artifact options from API.
 *
 * @param {number} compareNumber Which compare Version was selected, 1 or 2
 * @param {string} versionName Name of Version that was selected
 */
async function selectVersion(compareNumber: number, versionName: string) {
  if (compareNumber === 1) {
    versionSelection1.value = versionName;
    reportSelection1.value = "";
    report1.value = undefined;
  } else if (compareNumber === 2) {
    versionSelection2.value = versionName;
    reportSelection2.value = "";
    report2.value = undefined;
  }

  if (versionName == "") {
    return;
  }

  const artifacts = await getVersionArtifacts(
    queryModel as string,
    versionName,
  );

  if (!artifacts) {
    return;
  } else {
    const tempReportList: Array<ArtifactModel<ReportModel>> = [];
    const tempOptionsList: Array<SelectOption> = [];

    artifacts.forEach((artifact: ArtifactModel) => {
      if (artifact.body.artifact_type === "report") {
        tempReportList.push(artifact as ArtifactModel<ReportModel>);
        tempOptionsList.push(
          new SelectOption(
            artifact.header.identifier,
            artifact.header.identifier,
          ),
        );
      }
    });

    if (compareNumber === 1) {
      reportList1.value = tempReportList;
      reportOptions1.value = tempOptionsList;
    } else if (compareNumber === 2) {
      reportList2.value = tempReportList;
      reportOptions2.value = tempOptionsList;
    }
  }
}

/**
 * Handle selection of a new Report. Selects Report from reportList.
 *
 * @param {number} compareNumber Which compare Report was selected, 1 or 2
 * @param {string} reportName Name of Artifact that was selected
 */
async function selectReport(compareNumber: number, reportName: string) {
  if (compareNumber === 1) {
    report1.value = reportList1.value.find(
      (i) => i.header.identifier === reportName,
    );
  } else if (compareNumber === 2) {
    report2.value = reportList2.value.find(
      (i) => i.header.identifier === reportName,
    );
  }
}
</script>

<style>
.column {
  float: left;
  width: 50%;
}
/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>
