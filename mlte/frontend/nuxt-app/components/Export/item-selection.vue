<template>
  <UsaCard>
    <template #heading>
      <h3>Export Store Resources</h3>
    </template>

    <p>Select the resources to include in the export.</p>

    <div>
      <div class="grid-col-12 margin-bottom-3">
        <fieldset>
          <legend class="text-bold display-flex flex-justify width-full">
            <span>Models ({{ totalSelectedVersionsCount }})</span>
            <UsaButton variant="unstyled" @click="toggleAllModels">
              {{ isAllModelsSelected ? "Deselect All" : "Select All" }}
            </UsaButton>
          </legend>

          <div
            v-for="(versions, modelName) in availableModels"
            :key="modelName"
            class="margin-bottom-2"
          >
            <div class="text-bold margin-bottom-1 display-flex flex-justify">
              <span>{{ modelName }}</span>
              <UsaButton
                variant="unstyled"
                @click="toggleModelVersions(modelName)"
              >
                {{
                  isModelFullySelected(modelName)
                    ? "Deselect Versions"
                    : "Select All Versions"
                }}
              </UsaButton>
            </div>

            <div class="margin-left-2">
              <div
                v-for="version in versions"
                :key="version"
                class="margin-bottom-1 usa-checkbox"
              >
                <input
                  :id="`model-${modelName}-${version}`"
                  v-model="exportSpec.models[modelName]"
                  class="usa-checkbox__input"
                  type="checkbox"
                  :value="version"
                />
                <label
                  class="usa-checkbox__label"
                  :for="`model-${modelName}-${version}`"
                >
                  {{ version }}
                </label>
              </div>
            </div>
          </div>

          <p v-if="Object.keys(availableModels).length === 0">
            No models available.
          </p>
        </fieldset>
      </div>

      <div
        v-for="category in flatCategories"
        :key="category.id"
        class="grid-col-12 margin-bottom-3"
      >
        <fieldset>
          <legend class="text-bold display-flex flex-justify width-full">
            <span
              >{{ category.label }} ({{ exportSpec[category.id].length }})</span
            >
            <UsaButton variant="unstyled" @click="toggleSelectAll(category.id)">
              {{ isAllSelected(category.id) ? "Deselect All" : "Select All" }}
            </UsaButton>
          </legend>

          <div
            v-for="item in availableData[category.id]"
            :key="item"
            class="margin-bottom-1 usa-checkbox"
          >
            <input
              :id="`flat-${category.id}-${item}`"
              v-model="exportSpec[category.id]"
              type="checkbox"
              class="usa-checkbox__input"
              :value="item"
            />
            <label
              class="usa-checkbox__label"
              :for="`flat-${category.id}-${item}`"
            >
              {{ item }}
            </label>
          </div>

          <p v-if="availableData[category.id].length === 0">
            No {{ category.label.toLowerCase() }} available.
          </p>
        </fieldset>
      </div>
    </div>

    <template #footer>
      <div class="display-flex flex-justify-end">
        <UsaButton
          class="secondary-button"
          :disabled="totalSelectedCount === 0"
          @click="handleExportFile"
        >
          Export Selected ({{ totalSelectedCount }})
        </UsaButton>
      </div>
    </template>
  </UsaCard>
</template>

<script setup lang="ts">
const emit = defineEmits(["close"]);

type FlatCategoryKey = "users" | "custom_lists" | "catalogs";

const flatCategories = [
  { id: "users" as FlatCategoryKey, label: "Users" },
  { id: "custom_lists" as FlatCategoryKey, label: "Custom Lists" },
  { id: "catalogs" as FlatCategoryKey, label: "Catalogs" },
];

const availableModels = ref<Record<string, Array<string>>>({});
const availableData = ref<Record<FlatCategoryKey, string[]>>({
  users: [],
  custom_lists: [],
  catalogs: [],
});

const exportSpec = ref<ExportSpec>({
  models: {},
  users: [],
  custom_lists: [],
  catalogs: [],
});

async function populateFlatData(): Promise<Record<FlatCategoryKey, string[]>> {
  // Execute requests in parallel for maximum speed
  const [users, customLists, catalogs] = await Promise.all([
    getUserList(),
    getCustomListNames(),
    getCatalogList(),
  ]);

  return {
    users: users || [],
    custom_lists: customLists || [],
    catalogs: catalogs.map((c) => c.id),
  };
}

onMounted(async () => {
  const [models, flatData] = await Promise.all([
    populateModels(),
    populateFlatData(),
  ]);

  availableModels.value = models;
  availableData.value = flatData;

  Object.keys(models).forEach((modelName) => {
    if (!exportSpec.value.models[modelName]) {
      exportSpec.value.models[modelName] = [];
    }
  });
});

const totalSelectedVersionsCount = computed(() =>
  Object.values(exportSpec.value.models).reduce(
    (acc, versions) => acc + (versions?.length || 0),
    0,
  ),
);

async function populateModels(): Promise<Record<string, Array<string>>> {
  const data: Record<string, Array<string>> = {};
  const modelList: Array<string> = await getUserModels();
  for (const modelName of modelList) {
    data[modelName] = await getModelVersions(modelName);
  }
  return data;
}

function isModelFullySelected(modelName: string): boolean {
  const versions = availableModels.value[modelName] || [];
  return (
    versions.length > 0 &&
    (exportSpec.value.models[modelName]?.length || 0) === versions.length
  );
}

function toggleModelVersions(modelName: string) {
  const versions = availableModels.value[modelName] || [];
  if (isModelFullySelected(modelName)) {
    exportSpec.value.models[modelName] = [];
  } else {
    exportSpec.value.models[modelName] = [...versions];
  }
}

const isAllModelsSelected = computed(() => {
  const keys = Object.keys(availableModels.value);
  return keys.length > 0 && keys.every((key) => isModelFullySelected(key));
});

function toggleAllModels() {
  if (isAllModelsSelected.value) {
    Object.keys(availableModels.value).forEach((key) => {
      exportSpec.value.models[key] = [];
    });
  } else {
    Object.entries(availableModels.value).forEach(([key, versions]) => {
      exportSpec.value.models[key] = [...versions];
    });
  }
}

function isAllSelected(category: FlatCategoryKey): boolean {
  const items = availableData.value[category] || [];
  return exportSpec.value[category].length === items.length && items.length > 0;
}

function toggleSelectAll(category: FlatCategoryKey) {
  const items = availableData.value[category] || [];
  if (isAllSelected(category)) {
    exportSpec.value[category] = [];
  } else {
    exportSpec.value[category] = items.map((item) => item);
  }
}

const totalSelectedCount = computed(() => {
  const flatTotal =
    exportSpec.value.users.length +
    exportSpec.value.custom_lists.length +
    exportSpec.value.catalogs.length;
  return flatTotal + totalSelectedVersionsCount.value;
});

async function handleExportFile() {
  console.log(exportSpec.value);
  await exportStore(exportSpec.value);
  emit("close");
}
</script>
