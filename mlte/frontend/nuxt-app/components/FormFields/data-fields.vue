<template>
  <CollapsibleHeader v-model="displaySection" @change="displaySection = $event">
    <template #title> Data </template>
  </CollapsibleHeader>

  <div v-if="displaySection">
    <div class="input-group">
      <SubHeader :render-example="false">
        Data
        <template #info>
          Details of the data that will be used at any point during the
          development of the model.
        </template>
      </SubHeader>
      <hr />
      <div
        v-for="(dataItem, dataItemIndex) in props.modelValue"
        :key="dataItemIndex"
      >
        <h3 class="no-margin-sub-header" style="display: inline">
          Dataset {{ dataItemIndex + 1 }}
        </h3>
        <UsaButton
          v-if="!displayDataset[dataItemIndex]"
          class="secondary-button"
          @click="displayDataset[dataItemIndex] = true"
        >
          Show
        </UsaButton>
        <UsaButton
          v-else
          class="secondary-button"
          @click="displayDataset[dataItemIndex] = false"
        >
          Hide
        </UsaButton>
        <div v-if="displayDataset[dataItemIndex]">
          <div>
            <UsaTextarea v-model="dataItem.description" style="height: 5.5rem">
              <template #label>
                Dataset Description
                <InfoIcon>
                  Short description of the data set that will be used for model
                  development.
                  <br />
                  <br />
                  <i
                    >Example: Voice recordings from phone calls made to numbers
                    in the 412 area code.</i
                  >
                </InfoIcon>
              </template>
            </UsaTextarea>

            <UsaTextarea v-model="dataItem.purpose" style="height: 5.5rem">
              <template #label>
                Dataset Purpose
                <InfoIcon>
                  Purpose of the dataset in relation to the model.
                  <br />
                  <br />
                  <i>Example: Training, fine-tuning, etc.</i>
                </InfoIcon>
              </template>
            </UsaTextarea>

            <UsaTextInput v-model="dataItem.source">
              <template #label>
                Source
                <InfoIcon>
                  Where is the data coming from, e.g., Enterprise Data, Public
                  Data Source, <br />
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

          <UsaTextarea v-model="dataItem.access" style="height: 5.5rem">
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
          </UsaTextarea>

          <UsaTextarea v-model="dataItem.rights" style="height: 5.5rem">
            <template #label>
              Data Rights
              <InfoIcon>
                Are there particular ways in which the data can or cannot be
                used?
                <br />
                <br />
                <i
                  >Example: Given that data is classified it should be treated
                  as
                  <br />
                  such, e.g., not uploaded to any public servers or stored on
                  <br />
                  any non-authorized equipment.</i
                >
              </InfoIcon>
            </template>
          </UsaTextarea>

          <UsaTextarea v-model="dataItem.policies" style="height: 5.5rem">
            <template #label>
              Data Policies
              <InfoIcon>
                Are there policies that govern the data and its use, such as
                <br />
                Personally Identifiable Information [PII]?
                <br />
                <br />
                <i
                  >Example: Although the audio recordings are not associated to
                  a
                  <br />
                  person, post-analysis may associate them to a person and
                  <br />
                  therefore become PII.</i
                >
              </InfoIcon>
            </template>
          </UsaTextarea>

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
                distribution in the dataset. This may not be applicable in all
                cases.
              </template>
            </SubHeader>
            <UsaTextarea
              v-model="dataItem.labeling_method"
              style="height: 5.5rem"
            >
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
            </UsaTextarea>
            <div
              v-for="(label, labelIndex) in dataItem.labels"
              :key="labelIndex"
            >
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
                Include relevant information that is known about the data; fill
                out all sections below for each data field. This may not be
                applicable in all cases.
              </template>
            </SubHeader>
            <div
              v-for="(field, fieldIndex) in dataItem.fields"
              :key="fieldIndex"
            >
              <h3 class="no-margin-sub-header">
                Data Schema {{ fieldIndex + 1 }}
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
                        Expected values for field, e.g., any, range,
                        enumeration.
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
                        How to interpret missing values, e.g., null, empty
                        string.
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

          <DeleteButton
            class="margin-button"
            @click="deleteDataItem(dataItemIndex)"
          >
            Delete Dataset
          </DeleteButton>
          <hr />
        </div>
      </div>
      <AddButton class="margin-button" @click="addDataItem()">
        Add Dataset
      </AddButton>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Array<DataDescriptor>,
    required: true,
  },
});

// Provide hook for parent page to call addDataItem. Needed for descriptor import.
const parentAddDataItem = () => {
  addDataItem();
};

// Provide hook for parent page to call addLabel. Needed for descriptor import.
const parentAddLabel = (dataIndex: number) => {
  addLabel(dataIndex);
};

// Provide hook for parent page to call addField. Needed for descriptor import.
const parentAddField = (dataIndex: number) => {
  addField(dataIndex);
};

// Expose the hooks to parent page.
defineExpose({
  parentAddDataItem,
  parentAddLabel,
  parentAddField,
});

const displaySection = ref<boolean>(true);
const displayDataset = ref<Array<boolean>>([]);
const classificationOptions = useClassificationOptions();

props.modelValue.forEach(() => {
  displayDataset.value.push(true);
});

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

// Add DataDescriptor to data list.
function addDataItem() {
  props.modelValue.push(new DataDescriptor());
  displayDataset.value.push(true);
}

/**
 * Delete DataDescriptor from data list.
 *
 * @param {number} dataItemIndex Index of DataDescriptor to delete
 */
function deleteDataItem(dataItemIndex: number) {
  if (confirm("Are you sure you want to delete this data item?")) {
    props.modelValue.splice(dataItemIndex, 1);
  }
}

/**
 * Add LabelDescriptor to specified DataDescriptor.
 *
 * @param {number} dataItemIndex Index of DataDescriptor to add LabelDescriptor to.
 */
function addLabel(dataItemIndex: number) {
  props.modelValue[dataItemIndex].labels.push(new LabelDescriptor());
}

/**
 * Delete LabelDescriptor from list in DataDescriptor.
 *
 * @param {number} dataItemIndex Index of DataDescriptor
 * @param {number} labelIndex Index of LabelDescriptor to delete
 */
function deleteLabel(dataItemIndex: number, labelIndex: number) {
  if (confirm("Are you sure you want to delete this label?")) {
    props.modelValue[dataItemIndex].labels.splice(labelIndex, 1);
  }
}

/**
 * Add FieldDescriptor to specified DataDescriptor.
 *
 * @param {number} dataItemIndex Index of DataDescriptor to add FieldDescriptor to.
 */
function addField(dataItemIndex: number) {
  props.modelValue[dataItemIndex].fields.push(new FieldDescriptor());
}

/**
 * Delete FieldDescriptor from list in DataDescriptor.
 *
 * @param {number} dataItemIndex Index of DataDescriptor
 * @param {number} fieldIndex Index of FieldDescriptor to delete
 */
function deleteField(dataItemIndex: number, fieldIndex: number) {
  if (confirm("Are you sure you want to delete this field?")) {
    props.modelValue[dataItemIndex].fields.splice(fieldIndex, 1);
  }
}
</script>
