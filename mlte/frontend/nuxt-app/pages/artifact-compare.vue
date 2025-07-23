<template>
  <NuxtLayout name="base-layout">
    <title>Artifact Compare</title>
    <template #page-title>Artifact Compare</template>
    <h1 class="section-header">{{ queryModel }}</h1>

    <div class="half-line-input">
      <UsaSelect
        v-model="typeSelection"
        :options="typeOptions"
        @update:model-value="selectType($event)"
      >
        <template #label> Artifact Type </template>
      </UsaSelect>
    </div>
    <div class="row">
      <div class="column">
        <div class="half-line-input">
          <UsaSelect v-model="versionSelection1" :options="versionOptions">
            <template #label> Version 1 </template>
          </UsaSelect>
        </div>
        <div class="half-line-input">
          <UsaSelect v-model="suiteSelection1" :options="suiteOptions1">
            <template #label> Suite </template>
          </UsaSelect>
        </div>
        <div>
          {{ suite1 }}
        </div>
      </div>
      <div class="column">
        <div class="half-line-input">
          <UsaSelect v-model="versionSelection2" :options="versionOptions">
            <template #label> Version 2 </template>
          </UsaSelect>
        </div>
        <div class="half-line-input">
          <UsaSelect v-model="suiteSelection2" :options="suiteOptions2">
            <template #label> Suite </template>
          </UsaSelect>
        </div>
        <div>
          {{ suite2 }}
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const token = useCookie("token");
const queryModel = useRoute().query.model;

const typeOptions = ref<Array<SelectOption>>([
  new SelectOption("report", "Report"),
  new SelectOption("test_suite", "Test Suite"),
]);
const typeSelection = ref<string>("");
const versionOptions = ref<Array<SelectOption>>([]);
const versionSelection1 = ref<string>("");
const suiteOptions1 = ref([]);
const suiteSelection1 = ref<string>("");
const versionSelection2 = ref<string>("");
const suiteOptions2 = ref([]);
const suiteSelection2 = ref<string>("");

const suite1 = ref<TestSuiteModel>(new TestSuiteModel());
const suite2 = ref<TestSuiteModel>(new TestSuiteModel());

const modelVersions = await getModelVersions(
  token.value as string,
  queryModel as string,
);
if (modelVersions) {
  modelVersions.forEach((version: string) => {
    versionOptions.value.push(new SelectOption(version, version));
  });
}

async function selectType(artifactType: string) {
  if (artifactType == "report") {
  }
}

// async function selectVersion(suiteNumber: number, versionName: string){
//   /**
//    *
//    */
//   // if (versionName == ""){

//   // }

//   suite1.value = getTestSuite(token.value as string, queryModel, versionName, )
// }
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
