<template>
  <NuxtLayout name="base-layout">
    <title>Artifact Compare</title>
    <template #page-title>Artifact Compare</template>
    <h1 class="section-header">{{ queryModel }}</h1>

    <div class="half-line-input">
      <UsaSelect
        v-model="typeSelection"
        :options="typeOptions"
        @update:model-value="selectType()"
      >
        <template #label> Artifact Type </template>
      </UsaSelect>
    </div>
    <div class="row">
      <div class="column">
        <div class="half-line-input">
          <UsaSelect
            v-model="versionSelection1"
            :options="versionOptions"
            @update:model-value="selectVersion(1, $event)"
          >
            <template #label> Version 1 </template>
          </UsaSelect>
        </div>
        <div class="half-line-input">
          <UsaSelect
            v-model="artifactSelection1"
            :options="artifactOptions1"
            @update:model-value="selectArtifact(1, $event)"
          >
            <template #label> Artifact 1 </template>
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
            v-model="artifactSelection2"
            :options="artifactOptions2"
            @update:model-value="selectArtifact(2, $event)"
          >
            <template #label> Artifact 2 </template>
          </UsaSelect>
        </div>
      </div>
    </div>
    <div
      v-if="
        artifact1 &&
        artifact2 &&
        artifact1.body.artifact_type == 'test_suite' &&
        artifact2.body.artifact_type == 'test_suite'
      "
    >
      <TestSuiteCompare
        :version1="versionSelection1"
        :version2="versionSelection2"
        :test-suite1="artifact1"
        :test-suite2="artifact2"
      />
    </div>
    <div
      v-if="
        artifact1 &&
        artifact2 &&
        artifact1.body.artifact_type == 'report' &&
        artifact2.body.artifact_type == 'report'
      "
    >
      <ReportCompare
        :version1="versionSelection1"
        :version2="versionSelection2"
        :report1="artifact1"
        :report2="artifact2"
      />
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const queryModel = useRoute().query.model;
const typeOptions = ref<Array<SelectOption>>([
  new SelectOption("report", "Report"),
  new SelectOption("test_suite", "Test Suite"),
]);
const typeSelection = ref<string>("test_suite");
const versionOptions = ref<Array<SelectOption>>([]);

const versionSelection1 = ref<string>("");
const artifactList1 = ref<Array<ArtifactModel>>([]);
const artifactOptions1 = ref<Array<SelectOption>>([]);
const artifactSelection1 = ref<string>("");
const artifact1 = ref<ArtifactModel>();

const versionSelection2 = ref<string>("");
const artifactList2 = ref<Array<ArtifactModel>>([]);
const artifactOptions2 = ref<Array<SelectOption>>([]);
const artifactSelection2 = ref<string>("");
const artifact2 = ref<ArtifactModel>();

const modelVersions = await getModelVersions(queryModel as string);
if (modelVersions) {
  modelVersions.forEach((version: string) => {
    versionOptions.value.push(new SelectOption(version, version));
  });
}
selectVersion(1, modelVersions[modelVersions.length - 2]);
selectVersion(2, modelVersions[modelVersions.length - 1]);

// Reset Artifact selections, and load options for new Artifact type
async function selectType() {
  selectVersion(1, versionSelection1.value);
  selectVersion(2, versionSelection2.value);
  artifactSelection1.value = "";
  artifactSelection2.value = "";
  artifact1.value = undefined;
  artifact2.value = undefined;
}

/**
 * Handle selection of a new Version. Loads new Artifact options from API.
 *
 * @param {number} compareNumber Which compare Version was selected, 1 or 2
 * @param {string} versionName Name of Version that was selected
 */
async function selectVersion(compareNumber: number, versionName: string) {
  if (compareNumber === 1) {
    artifactSelection1.value = "";
    artifact1.value = undefined;
  } else if (compareNumber === 2) {
    artifactSelection2.value = "";
    artifact2.value = undefined;
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
  } else if (compareNumber === 1) {
    artifactList1.value = [];
    artifactOptions1.value = [];

    artifacts.forEach((artifact: ArtifactModel) => {
      if (typeSelection.value === artifact.body.artifact_type) {
        artifactList1.value.push(artifact);
        artifactOptions1.value.push(
          new SelectOption(
            artifact.header.identifier,
            artifact.header.identifier,
          ),
        );
      }
    });
  } else if (compareNumber === 2) {
    artifactList2.value = [];
    artifactOptions2.value = [];

    artifacts.forEach((artifact: ArtifactModel) => {
      if (typeSelection.value === artifact.body.artifact_type) {
        artifactList2.value.push(artifact);
        artifactOptions2.value.push(
          new SelectOption(
            artifact.header.identifier,
            artifact.header.identifier,
          ),
        );
      }
    });
  }
}

/**
 * Handle selection of a new Artifact. Selects Artifact from artifactList.
 *
 * @param {number} compareNumber Which compare Artifact was selected, 1 or 2
 * @param {string} artifactName Name of Artifact that was selected
 */
async function selectArtifact(compareNumber: number, artifactName: string) {
  if (compareNumber === 1) {
    artifact1.value = artifactList1.value.find(
      (i) => i.header.identifier === artifactName,
    );
  } else if (compareNumber === 2) {
    artifact2.value = artifactList2.value.find(
      (i) => i.header.identifier === artifactName,
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
