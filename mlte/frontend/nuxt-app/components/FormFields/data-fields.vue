<template>
  <h2 class="section-header">Data</h2>
  <div class="input-group">
    <SubHeader :render-example="false">
      Data
      <template #info>
        Details of the data that will influence model development efforts.
      </template>
    </SubHeader>
    <div
      v-for="(dataItem, dataItemIndex) in props.modelValue"
      :key="dataItemIndex"
    >
      <h3 class="no-margin-sub-header">Dataset {{ dataItemIndex + 1 }}</h3>
      <div>
        <UsaTextInput v-model="dataItem.description">
          <template #label>
            Dataset Description
            <InfoIcon>
              Short description of the data set that will be used for model
              development.
              <br />
              <br />
              <i
                >Example: Voice recordings from phone calls made to numbers in
                the 412 area code.</i
              >
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="dataItem.source">
          <template #label>
            Source
            <InfoIcon>
              Where is the data coming from, e.g., Enterprise Data, Public Data
              Source, <br />
              Synthetic Data?
              <br />
              <br />
              <i
                >Example: Company log data collected between 2023/01/01 and
                2023/12/31.</i
              >
            </InfoIcon>
          </template>
        </UsaTextInput>
      </div>

      <UsaSelect
        v-model="dataItem.classification"
        :options="classificationOptions"
      >
        <template #label>
          Data Classification
          <InfoIcon>
            What is the classification of the data?
            <br />
            <br />
            <i>Example: Classified, Unclassified, PHI, etc.</i>
          </InfoIcon>
        </template>
      </UsaSelect>

      <UsaTextInput v-model="dataItem.access">
        <template #label>
          Requirements and Constraints for Data Access
          <InfoIcon>
            How will the data be accessed? What accounts are needed?
            <br />
            <br />
            <i
              >Example: Data is stored on the "blue" server that requires an
              account on the "solid" network.</i
            >
          </InfoIcon>
        </template>
      </UsaTextInput>

      <div class="input-group" style="margin-top: 1em">
        <SubHeader>
          Labels and Distribution
          <template #example>
            <UsaTable
              :headers="labelModalHeaders"
              :rows="labelModalRows"
              borderless
              class="table"
            />
          </template>
          <template #info>
            If data is labeled, include information about labels and their
            distribution in the dataset.
          </template>
        </SubHeader>
        <UsaTextInput v-model="dataItem.labeling_method">
          <template #label>
            Labeling Method
            <InfoIcon>
              How data was labeled, e.g., hand labeled by expert, <br />
              labeled by automated process.
              <br />
              <br />
              <i>Example: Hand labeled by single domain expert.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>
        <div v-for="(label, labelIndex) in dataItem.labels" :key="labelIndex">
          <div class="inline-input-left">
            <UsaTextInput v-model="label.name">
              <template #label>
                Label Name
                <InfoIcon> Label in data set. </InfoIcon>
              </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-left">
            <UsaTextInput v-model="label.description">
              <template #label>
                Label Description
                <InfoIcon> Short description of label. </InfoIcon>
              </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-right">
            <UsaTextInput v-model="label.percentage" type="number">
              <template #label>
                Percentage
                <InfoIcon>
                  Percentage of data elements with that label.
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>
          <div class="inline-button">
            <DeleteButton @click="deleteLabel(dataItemIndex, labelIndex)">
              Delete Label
            </DeleteButton>
          </div>
        </div>

        <AddButton class="margin-button" @click="addLabel(dataItemIndex)">
          Add Additional Label
        </AddButton>
      </div>

      <div class="input-group" style="margin-top: 1em">
        <SubHeader>
          Data Schema
          <template #example>
            <UsaTable
              :headers="dataModalHeaders"
              :rows="dataModalRows"
              borderless
              class="table"
            />
          </template>
          <template #info>
            Include relevant information that is known about the data; fill out
            all sections below for each data field.
          </template>
        </SubHeader>
        <div v-for="(field, fieldIndex) in dataItem.fields" :key="fieldIndex">
          <h3 class="no-margin-sub-header">
            Data Schema {{ dataItemIndex + 1 }} - {{ fieldIndex + 1 }}
          </h3>
          <div>
            <div class="inline-input-left">
              <UsaTextInput v-model="field.name">
                <template #label>
                  Field Name
                  <InfoIcon> Field name. </InfoIcon>
                </template>
              </UsaTextInput>
            </div>

            <div class="inline-input-right">
              <UsaTextInput v-model="field.description">
                <template #label>
                  Field Description
                  <InfoIcon> Short field description. </InfoIcon>
                </template>
              </UsaTextInput>
            </div>
          </div>

          <div>
            <div class="inline-input-left">
              <UsaTextInput v-model="field.type">
                <template #label>
                  Field Type
                  <InfoIcon>
                    Field type, e.g., number, string, Boolean, data, image,
                    audio.
                  </InfoIcon>
                </template>
              </UsaTextInput>
            </div>

            <div class="inline-input-right">
              <UsaTextInput v-model="field.expected_values">
                <template #label>
                  Expected Values
                  <InfoIcon>
                    Expected values for field, e.g., any, range, enumeration.
                  </InfoIcon>
                </template>
              </UsaTextInput>
            </div>
          </div>

          <div>
            <div class="inline-input-left">
              <UsaTextInput v-model="field.missing_values">
                <template #label>
                  Handling Missing Values
                  <InfoIcon>
                    How to interpret missing values, e.g., null, empty string.
                  </InfoIcon>
                </template>
              </UsaTextInput>
            </div>

            <div class="inline-input-right">
              <UsaTextInput v-model="field.special_values">
                <template #label>
                  Handling Special Values
                  <InfoIcon>
                    How to interpret special values, e.g., 999, N/A.
                  </InfoIcon>
                </template>
              </UsaTextInput>
            </div>
          </div>
          <DeleteButton
            class="margin-button"
            @click="deleteField(dataItemIndex, fieldIndex)"
          >
            Delete Field
          </DeleteButton>
          <hr />
        </div>

        <AddButton class="margin-button" @click="addField(dataItemIndex)">
          Add Additional Field
        </AddButton>
      </div>

      <UsaTextInput v-model="dataItem.rights">
        <template #label>
          Data Rights
          <InfoIcon>
            Are there particular ways in which the data can or cannot be used?
            <br />
            <br />
            <i
              >Example: Given that data is classified it should be treated as
              <br />
              such, e.g., not uploaded to any public servers or stored on
              <br />
              any non-authorized equipment.</i
            >
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextInput v-model="dataItem.policies">
        <template #label>
          Data Policies
          <InfoIcon>
            Are there policies that govern the data and its use, such as
            <br />
            Personally Identifiable Information [PII]?
            <br />
            <br />
            <i
              >Example: Although the audio recordings are not associated to a
              <br />
              person, post-analysis may associate them to a person and <br />
              therefore become PII.</i
            >
          </InfoIcon>
        </template>
      </UsaTextInput>

      <DeleteButton
        class="margin-button"
        @click="deleteDataItem(dataItemIndex)"
      >
        Delete Dataset
      </DeleteButton>
      <hr />
    </div>
    <AddButton class="margin-button" @click="addDataItem()">
      Add Dataset
    </AddButton>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
    default: [
      {
        description: "",
        source: "",
        classification: "unclassified",
        access: "",
        labeling_method: "",
        labels: [
          {
            name: "",
            description: "",
            percentage: 0,
          },
        ],
        fields: [
          {
            name: "",
            description: "",
            type: "",
            expected_values: "",
            missing_values: "",
            special_values: "",
          },
        ],
        rights: "",
        policies: "",
      },
    ],
  },
});

const parentAddDataItem = () => {
  addDataItem();
};

const parentAddLabel = (dataIndex: number) => {
  addLabel(dataIndex);
};

const parentAddField = (dataIndex: number) => {
  addField(dataIndex);
};

defineExpose({
  parentAddDataItem,
  parentAddLabel,
  parentAddField,
});

const classificationOptions = useClassificationOptions();

const labelModalHeaders = ref([
  { id: "labelName", label: "Label Name", sortable: false },
  { id: "labelDescription", label: "Label Description", sortable: false },
  { id: "percentage", label: "Percentage", sortable: false },
]);
const labelModalRows = ref([
  {
    id: "rock",
    labelName: "Rock",
    labelDescription: "Includes all rock genres",
    percentage: 24,
  },
  {
    id: "classical",
    labelName: "Classical",
    labelDescription: "Includes traditional and crossover",
    percentage: 7,
  },
  {
    id: "pop",
    labelName: "Pop",
    labelDescription: "Pop genre",
    percentage: 28,
  },
  {
    id: "jazz",
    labelName: "Jazz",
    labelDescription: "Includes classical, latin, and other forms of jazz",
    percentage: 16,
  },
  {
    id: "rap",
    labelName: "Rap",
    labelDescription: "Rap genre (not R&B)",
    percentage: 9,
  },
  {
    id: "dance",
    labelName: "Dance",
    labelDescription: "Includes all dance variants (e.g., house, techno)",
    percentage: 10,
  },
  {
    id: "other",
    labelName: "Other",
    labelDescription: "Any genre not covered by the above labels",
    percentage: 6,
  },
]);

const dataModalHeaders = ref([
  { id: "fieldName", label: "Field Name", sortable: false },
  { id: "fieldDescription", label: "Field Description", sortable: false },
  { id: "fieldType", label: "Field Type", sortable: false },
  { id: "expectedValues", label: "Expected Values", sortable: false },
  { id: "missingValues", label: "Handling Missing Values", sortable: false },
  { id: "specialValues", label: "Handling Special Values", sortable: false },
]);
const dataModalRows = ref([
  {
    id: "idRecording",
    fieldName: "ID Recording",
    fieldDescription: "Unique ID for audio recording",
    fieldType: "String",
    expectedValues: "Alphanumeric string",
    missingValues: "If ID is missing it should be discarded",
    specialValues: "No special values",
  },
  {
    id: "audioRecording",
    fieldName: "Audio Recording",
    fieldDescription: "Audio recording file",
    fieldType: "Audio",
    expectedValues: "Non-empty audio file",
    missingValues: "If audio file is missing it should be discarded",
    specialValues: "No special values",
  },
  {
    id: "dateRecording",
    fieldName: "Date Recording",
    fieldDescription: "Date audio was recorded",
    fieldType: "Date",
    expectedValues: "Between 2023/01/01 and 2023/12/31",
    missingValues:
      "If date is null or empty attempt to find date. If not possible then change to 00/00/0000 to simply use as a data point",
    specialValues:
      "00/00/0000 would indicate that the file did not have an associated date",
  },
]);

function addDataItem() {
  props.modelValue.push({
    description: "",
    source: "",
    classification: "unclassified",
    access: "",
    labeling_method: "",
    labels: [
      {
        name: "",
        description: "",
        percentage: 0,
      },
    ],
    fields: [
      {
        name: "",
        description: "",
        type: "",
        expected_values: "",
        missing_values: "",
        special_values: "",
      },
    ],
    rights: "",
    policies: "",
  });
}

function deleteDataItem(dataItemIndex: number) {
  if (confirm("Are you sure you want to delete this data item?")) {
    props.modelValue.splice(dataItemIndex, 1);
  }
}

function addLabel(dataItemIndex: number) {
  props.modelValue[dataItemIndex].labels.push({
    name: "",
    description: "",
    percentage: 0,
  });
}

function deleteLabel(dataItemIndex: number, labelIndex: number) {
  if (confirm("Are you sure you want to delete this label?")) {
    props.modelValue[dataItemIndex].labels.splice(labelIndex, 1);
  }
}

function addField(dataItemIndex: number) {
  props.modelValue[dataItemIndex].fields.push({
    name: "",
    description: "",
    type: "",
    expected_values: "",
    missing_values: "",
    special_values: "",
  });
}

function deleteField(dataItemIndex: number, fieldIndex: number) {
  if (confirm("Are you sure you want to delete this field?")) {
    props.modelValue[dataItemIndex].fields.splice(fieldIndex, 1);
  }
}
</script>
