<template>
  <NuxtLayout name="base-layout">
    <template #sidebar>
      <div style="padding-top: 255px">
        TEC Import
        <hr />
        <div class="usa-form-group">
          <label class="usa-label"> System Context </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'System Context')"
          />

          <label class="usa-label"> Raw Data </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'Raw Data')"
          />

          <label class="usa-label"> Development Environment </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'Development Environment')"
          />

          <label class="usa-label"> Production Environment </label>
          <input
            class="usa-file-input"
            type="file"
            accept=".json"
            @change="descriptorUpload($event, 'Production Environment')"
          />
        </div>
      </div>
    </template>

    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">How to use the Negotiation Card</h1>
    <p>
      Teams should work through as many of the following items before starting
      model development. The Negotiation Card can and should be revisited at any
      negotiation point. Teams should refer to this Negotiation Card during
      development to ensure they capture all relevant critical aspects of the
      model and system. Hover over the black information icons next to each
      field to get more information about that field. Click on the Example
      button to see specific examples for a section.
    </p>

    <UsaTextInput
      v-if="useRoute().query.artifactId === undefined"
      v-model="userInputArtifactId"
    >
      <template #label>
        Artifact ID
        <InfoIcon>
          The Artifact ID this negotiation card <br />
          will be saved under upon submission.
        </InfoIcon>
      </template>
    </UsaTextInput>
    <div v-else>
      <h3>Last Modified by:</h3>
      {{ form.creator }} - {{ form.timestamp }}
    </div>

    <h2 class="section-header">System Information</h2>
    <div class="input-group">
      <SubHeader :render-example="false">
        Goals
        <template #info>
          Goals or objectives that the model is going to help satisfy as part of
          the system.
        </template>
      </SubHeader>
      <div v-for="(goal, goalIndex) in form.system.goals" :key="goalIndex">
        <h3 class="no-margin-sub-header">Goal {{ goalIndex + 1 }}</h3>
        <UsaTextInput v-model="goal.description">
          <template #label>
            Goal Description
            <InfoIcon>
              Short description for the goal.
              <br />
              <br />
              <i
                >Example: Identify voice recordings that belong to a given
                person of interest.</i
              >
            </InfoIcon>
          </template>
        </UsaTextInput>

        <SubHeader :render-example="false" :render-info="false">
          Metrics
        </SubHeader>
        <div v-for="(metric, metricIndex) in goal.metrics" :key="metricIndex">
          <div class="inline-input-left">
            <UsaTextInput v-model="metric.description">
              <template #label>
                Description
                <InfoIcon>
                  Performance metric that captures the system's ability to
                  accomplish the goal,<br />
                  i.e., acceptance criteria for determining that the model is
                  performing correctly.
                  <br />
                  <br />
                  <i>Example: Accuracy > 90%</i>
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-right">
            <UsaTextInput v-model="metric.baseline">
              <template #label>
                Baseline Source
                <InfoIcon>
                  Indicates where the performance metric goal comes from, or why
                  it is <br />
                  believed to be achievable.
                  <br />
                  <br />
                  <i
                    >Example: Human accuracy for matching voices is ~60% as
                    stated in the paper<br />
                    by Smith et al.</i
                  ><br />
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>
          <div class="inline-button">
            <DeleteButton @click="deleteMetric(goalIndex, metricIndex)">
              Delete Metric
            </DeleteButton>
          </div>
        </div>
        <AddButton class="margin-button" @click="addMetric(goalIndex)">
          Add Metric
        </AddButton>
        <DeleteButton @click="deleteGoal(goalIndex)">
          Delete Goal
        </DeleteButton>
        <hr />
      </div>

      <AddButton class="margin-button" @click="addGoal()"> Add Goal </AddButton>
    </div>

    <UsaSelect v-model="form.system.problem_type" :options="problemTypeOptions">
      <template #label>
        ML Problem Type
        <InfoIcon>
          Type of ML problem that the model is intended to solve.
          <br />
          <br />
          <i
            >Example: Classification, Clustering, Detection, and others in
            drop-down list.</i
          >
        </InfoIcon>
      </template>
    </UsaSelect>

    <UsaTextInput v-model="form.system.task">
      <template #label>
        ML Task
        <InfoIcon>
          Well-defined task that model is expected to perform, or problem that
          the model is expected to solve.
          <br />
          <br />
          <i>Example: Match voice recordings spoken by the same person.</i>
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.usage_context">
      <template #label>
        Usage Context
        <InfoIcon>
          Who is intended to utilize the system/model; how the results of the
          model are <br />
          going to be used by end users or in the context of a larger system.
          <br />
          <br />
          <i
            >Example: Model results are consumed by a system component that
            shows
            <br />
            an intel analyst a list of matching voice recordings.</i
          >
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.target_audience">
      <template #label>
        Target Audience
        <InfoIcon>
          Who is intended to utilize the system/model?
          <br />
          <br />
          <i
            >Example: health care providers, etc.
            <br />
            </i
          >
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.risks.fp">
      <template #label>
        False Positive Risk
        <InfoIcon>
          What is the risk of producing a false positive?
          <br />
          <br />
          <i
            >Example: Incorrect positive results will cause extra work for the
            <br />
            intel analyst that needs to analyze every recording flagged by the
            model.</i
          >
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.risks.fn">
      <template #label>
        False Negative Risk
        <InfoIcon>
          What is the risk of producing a false negative?
          <br />
          <br />
          <i
            >Example: Incorrect negative results means that the model will
            <br />
            not flag suspicious recordings, which means that intel analysts
            <br />
            might miss information that is crucial to an investigation.</i
          >
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.risks.other">
      <template #label>
        Other Risks of Producing Incorrect Results
        <InfoIcon>
          What are other risks of producing incorrect results?
        </InfoIcon>
      </template>
    </UsaTextInput>

    <h2 class="section-header">Data</h2>
    <div class="input-group">
      <SubHeader :render-example="false">
        Data
        <template #info>
          Details of the data that will influence model development efforts.
        </template>
      </SubHeader>
      <div v-for="(dataItem, dataItemIndex) in form.data" :key="dataItemIndex">
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
                Delete label
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
              out all sections below for each data field.
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

    <h2 class="section-header">Model Information</h2>
    <div class="input-group">
      <SubHeader>
        Development Compute Resources
        <template #example>
          GPUs = 2, CPUs = 1, Memory = 512 MB, Storage = 1 GB
        </template>
        <template #info>
          Describe the amount and type of compute resources needed for training.
        </template>
      </SubHeader>
      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.development.resources.gpu">
            <template #label> Graphics Processing Units (GPUs) </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.development.resources.cpu">
            <template #label> Central Processing Units (CPUs) </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.development.resources.memory">
            <template #label> Memory </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.development.resources.storage">
            <template #label> Storage </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <UsaTextarea v-model="form.model.production.deployment_platform">
      <template #label>
        Deployment Platform
        <InfoIcon>
          Describe the deployment platform for the model, e.g., local server,
          <br />
          cloud server, embedded platform.
          <br />
          <br />
          <i>Example: Local server due to data classification issues.</i>
        </InfoIcon>
      </template>
    </UsaTextarea>

    <UsaTextarea
      v-model="form.model.production.capability_deployment_mechanism"
    >
      <template #label>
        Capability Deployment Mechanism
        <InfoIcon>
          Describe how the model capabilities will be made available, <br />
          e.g., API, user facing, data feed.
          <br />
          <br />
          <i
            >Example: The model will expose an API so that it can be called
            <br />
            from the intel analyst UI.</i
          >
        </InfoIcon>
      </template>
    </UsaTextarea>

    <div class="input-group" style="margin-top: 1em">
      <SubHeader>
        Input Specification
        <template #example>
          <UsaTable
            :headers="inputModalHeaders"
            :rows="inputModalRows"
            borderless
            class="table"
          />
        </template>
        <template #info>
          Describe the input data type and format needed for model to conduct
          inference.
        </template>
      </SubHeader>
      <UsaTextInput v-model="form.model.production.interface.input.name">
        <template #label>
          Input Name
          <InfoIcon>
            Input name.
            <br />
            <br />
            <i>Example: Audio Recording.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextarea v-model="form.model.production.interface.input.description">
        <template #label>
          Input Description
          <InfoIcon>
            Short input description.
            <br />
            <br />
            <i>Example: Audio recording file for matching.</i>
          </InfoIcon>
        </template>
      </UsaTextarea>

      <UsaTextInput v-model="form.model.production.interface.input.type">
        <template #label>
          Input Type
          <InfoIcon>
            Field type, e.g., number, string, Boolean, data, image, audio.
            <br />
            <br />
            <i>Example: Audio.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>
    </div>

    <div class="input-group" style="margin-top: 1em">
      <SubHeader>
        Output Specification
        <template #example>
          <UsaTable
            :headers="outputModalHeaders"
            :rows="outputModalRows"
            borderless
            class="table"
          />
        </template>
        <template #info>
          Describe the output format and specification needed for the system to
          ingest model results.
        </template>
      </SubHeader>
      <UsaTextInput v-model="form.model.production.interface.output.name">
        <template #label>
          Output Name
          <InfoIcon>
            Output name.
            <br />
            <br />
            <i>Example: Matching recordings.</i>
          </InfoIcon>
        </template>
      </UsaTextInput>

      <UsaTextarea v-model="form.model.production.interface.output.description">
        <template #label>
          Output Description
          <InfoIcon>
            Short output description.
            <br />
            <br />
            <i>Example: Set of matching recordings from the database.</i>
          </InfoIcon>
        </template>
      </UsaTextarea>

      <UsaTextInput v-model="form.model.production.interface.output.type">
        <template #label>
          Output Type
          <InfoIcon>
            Field type, e.g., number, string, Boolean, data, image, audio.
            <br />
            <br />
            <i
              >Example: Vector of Strings with IDs of matching recordings — an
              empty <br />
              vector means that there were no matches.</i
            >
          </InfoIcon>
        </template>
      </UsaTextInput>
    </div>

    <div class="input-group" style="margin-top: 1em">
      <SubHeader>
        Production Compute Resources
        <template #example>
          Example: GPUs = 2, CPUs = 2, Memory = 256 MB, Storage = 512 MB
        </template>
        <template #info>
          Describe the amount and type of compute resources needed for
          inference.
        </template>
      </SubHeader>
      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.production.resources.gpu">
            <template #label> Graphics Processing Units (GPUs) </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.production.resources.cpu">
            <template #label> Central Processing Units (CPUs) </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.production.resources.memory">
            <template #label> Memory </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.production.resources.storage">
            <template #label> Storage </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

  <br/>
    <h2 class="section-header">System Requirements</h2>
      <!-- Priority Legend  -->
    <br/>
    <div class="horizontal-legend">
      <div class="legend-item">
        <span class="circle top-priority"></span>
        <p>Top Priority</p>
    </div>
    
    <div class="legend-item">
        <span class="circle mild-priority"></span>
        <p>Mild Priority</p>
    </div>

    <div class="legend-item">
      <span class="circle low-priority"></span>
      <p>Low Priority</p>
    </div>
    </div>

    <!-- End Priority Legend  -->

    <br/>

    <div class="input-group">
    <!-- List of requirements -->
    <br/>
    <Accordion title="Inference Latency">
      <template #content>
        <!-- TODO: pull data from these fields if it is modified while filling out the form-->
         <!-- TODO: Make those fields mandatory in the form -->
        <InferenceLat MLTask={{ form.system.task }} :usageContext="form.system.usage_context" />
      </template>
    </Accordion>

 

    <Accordion title="Explainability">
      <template #content>
        <Explainability></Explainability>
      </template>
    </Accordion>

    </div>
    <br/>

    <!--TODO: Delete Prior Version -->
    <div class="input-group">
      <SubHeader :render-info="false">
        Requirements
        <template #example>
          <UsaTable
            :headers="systemModalHeaders"
            :rows="systemModalRows"
            borderless
            class="table"
          />
        </template>
      </SubHeader>
      <div
        v-for="(requirement, requirementIndex) in form.system_requirements"
        :key="requirementIndex"
      >
        <h3 class="no-margin-sub-header">
          Requirement {{ requirementIndex + 1 }}
        </h3>
        <p class="input-group" style="padding-top: 10px; padding-bottom: 10px">
          <b>Scenario for {{ requirement.quality }}: </b>
          >{{ requirement.stimulus }} from {{ requirement.source }} during
          {{ requirement.environment }}. {{ requirement.response }}
          {{ requirement.measure }}.
        </p>
        <UsaTextInput v-model="requirement.quality">
          <template #label>
            System Quality
            <InfoIcon>
              System property by which the model will be evaluated <br />
              (e.g., Accuracy, Performance, Robustness, Fairness, Resource
              Consumption).
              <br />
              <br />
              <i>Example: Response time.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="requirement.stimulus">
          <template #label>
            Stimulus
            <InfoIcon>
              A condition arriving at the system/model (e.g., data,
              <br />
              event, user operation, attack, request for modification,
              <br />
              completion of a unit of development).
              <br />
              <br />
              <i>Example: Model receives an audio recording.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="requirement.source">
          <template #label>
            Source of Stimulus
            <InfoIcon>
              Where the stimulus comes from (e.g., data source, <br />
              internal/external user, internal/external computer system,
              <br />
              sensor).
              <br />
              <br />
              <i>Example: Intel analyst application.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="requirement.environment">
          <template #label>
            Environment
            <InfoIcon>
              Set of circumstances in which the scenario takes place <br />
              (e.g., normal operations, overload condition, startup, development
              time).
              <br />
              <br />
              <i>Example: Normal operations.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="requirement.response">
          <template #label>
            Response
            <InfoIcon>
              Activity that occurs as the result of the arrival of the
              <br />
              stimulus (e.g., inference, process event, deny access, <br />
              implement modification, test).
              <br />
              <br />
              <i>Example: Inference time.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="requirement.measure">
          <template #label>
            Response Measure
            <InfoIcon>
              Measures used to determine that the responses enumerated for
              <br />
              the scenario have been achieved (e.g., statistical property,
              <br />
              latency, throughput, execution time, effort).
              <br />
              <br />
              <i>Example: At most 5 seconds.</i>
            </InfoIcon>
          </template>
        </UsaTextInput>
        <DeleteButton
          class="margin-button"
          @click="deleteRequirement(requirementIndex)"
        >
          Delete Requirement
        </DeleteButton>
        <hr />
      </div>
      <AddButton class="margin-button" @click="addRequirement()">
        Add Requirement
      </AddButton>
    </div>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/here",
    text: "Negotiation Card",
  },
]);

const userInputArtifactId = ref("");
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);

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

const inputModalHeaders = ref([
  { id: "inputName", label: "Input Name", sortable: false },
  { id: "inputDescription", label: "Input Description", sortable: false },
  { id: "inputType", label: "Input Type", sortable: false },
]);
const inputModalRows = ref([
  {
    id: "audio",
    inputName: "Audio Recording",
    inputDescription: "Audio recording file for matching",
    inputType: "Audio",
  },
]);

const outputModalHeaders = ref([
  { id: "outputName", label: "Output Name", sortable: false },
  { id: "outputDescription", label: "Output Description", sortable: false },
  { id: "outputType", label: "Output Type", sortable: false },
]);
const outputModalRows = ref([
  {
    id: "recording",
    outputName: "Matching Recordings",
    outputDescription: "Set of matching recordings from the database",
    outputType:
      "Vector of Strings with IDs of matching recordings — an empty vector means that there were no matches",
  },
]);

const systemModalHeaders = ref([
  { id: "systemQuality", label: "System Quality", sortable: false },
  { id: "stimulus", label: "Stimulus", sortable: false },
  { id: "source", label: "Source of Stimulus", sortable: false },
  { id: "environment", label: "Environment", sortable: false },
  { id: "response", label: "Response", sortable: false },
  { id: "measure", label: "Response Measure", sortable: false },
]);
const systemModalRows = ref([
  {
    id: "responseTime",
    systemQuality: "Response Time",
    stimulus: "Model receives an audio recording",
    source: "Intel analyst application",
    environment: "Normal operations",
    response: "Inference time",
    measure: "At most 5 seconds",
  },
  {
    id: "fairness",
    systemQuality: "Fairness - Model Impartial to Photo Location",
    stimulus: "Model receives a picture taken at the garden",
    source: "Flower identification application",
    environment: "Normal operations",
    response: "Correct identification of flowers regardless of garden location",
    measure: "At least 90% of the time",
  },
  {
    id: "robustness",
    systemQuality: "Robustness - Model Robust to Noise (Image Blur)",
    stimulus:
      "Model receives a picture taken at the garden and it is a bit blurry",
    source: "Flower identification application",
    environment: "Normal operations",
    response: "Correct identification of flowers",
    measure: "Same rate as non-blurry images",
  },
  {
    id: "performance",
    systemQuality: "Performance on Operational Platform",
    stimulus: "Model receives a picture taken at a garden",
    source: "Flower identification application",
    environment: "Normal operations",
    response:
      "Model will need to run on the devices loaned out by the garden centers to visitors. These are small, inexpensive devices with limited CPU power, as well as limited memory and disk space (512 MB and 128 GB, respectively).",
    measure: "No errors due to unavailable resources",
  },
]);

const form = ref({
  creator: "",
  timestamp: "",
  system: {
    goals: [
      {
        description: "",
        metrics: [
          {
            description: "",
            baseline: "",
          },
        ],
      },
    ],
    problem_type: "classification",
    task: "",
    usage_context: "",
    risks: {
      fp: "",
      fn: "",
      other: "",
    },
  },
  data: [
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
  model: {
    development: {
      resources: {
        gpu: "0",
        cpu: "0",
        memory: "0",
        storage: "0",
      },
    },
    production: {
      deployment_platform: "",
      capability_deployment_mechanism: "",
      interface: {
        input: {
          name: "",
          description: "",
          type: "",
        },
        output: {
          name: "",
          description: "",
          type: "",
        },
      },
      resources: {
        gpu: "0",
        cpu: "0",
        memory: "0",
        storage: "0",
      },
    },
  },
  system_requirements: [
    {
      quality: "<System Quality>",
      stimulus: "<Stimulus>",
      source: "<Source>",
      environment: "<Environment>",
      response: "<Response>",
      measure: "<Response Measure>",
    },
  ],
});

// TODO: Pull these from the schema
const problemTypeOptions = [
  { value: "classification", text: "Classification" },
  { value: "clustering", text: "Clustering" },
  { value: "detection", text: "Detection" },
  { value: "trend", text: "Trend" },
  { value: "alert", text: "Alert" },
  { value: "forecasting", text: "Forecasting" },
  { value: "content_generation", text: "Content Generation" },
  { value: "benchmarking", text: "Benchmarking" },
  { value: "goals", text: "Goals" },
  { value: "other", text: "Other" },
];

// TODO: Pull these from the schema
const classificationOptions = [
  { value: "unclassified", text: "Unclassified" },
  {
    value: "cui",
    text: "Controlled Unclassified Information (CUI)",
  },
  { value: "classified", text: "Classified" },
  {
    value: "pii",
    text: "Personally Identifiable Information (PII)",
  },
  {
    value: "phi",
    text: "Protected Health Information (PHI)",
  },
  { value: "other", text: "Other" },
];

if (useRoute().query.artifactId !== undefined) {
  const model = useRoute().query.model;
  const version = useRoute().query.version;
  const artifactId = useRoute().query.artifactId;

  await useFetch(
    config.public.apiPath +
      "/model/" +
      model +
      "/version/" +
      version +
      "/artifact/" +
      artifactId,
    {
      retry: 0,
      method: "GET",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (isValidNegotiation(response._data)) {
          form.value.creator = response._data.header.creator;
          form.value.timestamp = new Date(
            response._data.header.timestamp * 1000,
          ).toLocaleString("en-US");
          form.value.system = response._data.body.system;
          form.value.data = response._data.body.data;
          form.value.model = response._data.body.model;
          form.value.system_requirements =
            response._data.body.system_requirements;

          const problemType = response._data.body.system.problem_type;
          if (
            problemTypeOptions.find((x) => x.value === problemType)?.value !==
            undefined
          ) {
            form.value.system.problem_type = problemTypeOptions.find(
              (x) => x.value === problemType,
            )?.value;
          }

          response._data.data.forEach((item) => {
            const classification = item.classification;
            if (
              classificationOptions.find((x) => x.value === classification)
                ?.value !== undefined
            ) {
              item.classification = classificationOptions.find(
                (x) => x.value === classification,
              )?.value;
            }
          });
        }
      },
      onResponseError() {
        responseErrorAlert();
      },
    },
  );
}

async function submit() {
  const model = useRoute().query.model;
  const version = useRoute().query.version;

  let identifier = "";
  if (useRoute().query.artifactId === undefined) {
    identifier = userInputArtifactId.value;
  } else {
    identifier = useRoute().query.artifactId?.toString();
  }

  // Construct the object to be submitted to the backend here
  const artifact = {
    header: {
      identifier,
      type: "negotiation_card",
      timestamp: -1,
      creator: "",
    },
    body: {
      artifact_type: "negotiation_card",
      system: form.value.system,
      data: form.value.data,
      model: form.value.model,
      system_requirements: form.value.system_requirements,
    },
  };

  if (isValidNegotiation(artifact)) {
    try {
      await $fetch(
        config.public.apiPath +
          "/model/" +
          model +
          "/version/" +
          version +
          "/artifact",
        {
          retry: 0,
          method: "POST",
          headers: {
            Authorization: "Bearer " + token.value,
          },
          body: {
            artifact,
            force: forceSaveParam.value,
            parents: false,
          },
          onRequestError() {
            requestErrorAlert();
          },
          onResponseError({ response }) {
            if (response.status === 409) {
              conflictErrorAlert();
            } else {
              responseErrorAlert();
            }
          },
        },
      );
      successfulSubmission("negotiation card", identifier);
      forceSaveParam.value = true;
    } catch (error) {
      console.log("Error in fetch.");
      console.log(error);
    }
  } else {
    console.log("Invalid document attempting to be submitted.");
  }
}

function descriptorUpload(event: Event, descriptorName: string) {
  const target = event.target as HTMLInputElement;
  const file = target.files![0];
  if (file !== null) {
    const reader = new FileReader();
    reader.onload = (inputFile) => {
      try {
        const document = JSON.parse((inputFile.target!.result as string) ?? "");
        if (descriptorName === "System Context") {
          document.goals.forEach(
            (goal: {
              id: string;
              goal: string;
              metric: string;
              baseline: string;
            }) => {
              addGoal();
              const lastGoalIndex = form.value.system.goals.length - 1;

              form.value.system.goals[lastGoalIndex].description = goal.goal;
              form.value.system.goals[lastGoalIndex].metrics[0].description =
                goal.metric;
              form.value.system.goals[lastGoalIndex].metrics[0].baseline =
                goal.baseline;
            },
          );
          form.value.system.task = document.task;
          form.value.system.problem_type = document.ml_problem_type.ml_problem;
          form.value.system.usage_context = document.usage_context;
          form.value.system.risks.fp = document.risks.risk_fp;
          form.value.system.risks.fn = document.risks.risk_fn;
          form.value.system.risks.other = document.risks.risk_other;
        } else if (descriptorName === "Raw Data") {
          addDataItem();
          const lastDataIndex = form.value.data.length - 1;

          let dataSourcesStr = "";
          document.data_sources.forEach(
            (
              source: { data_source: string; other_source: string },
              i: number,
            ) => {
              if (source.data_source === "Other") {
                dataSourcesStr += source.other_source;
              } else {
                dataSourcesStr += source.data_source;
              }

              if (i + 1 < document.data_sources.length) {
                dataSourcesStr += ", ";
              }
            },
          );
          form.value.data[lastDataIndex].source = dataSourcesStr;

          form.value.data[lastDataIndex].labels.splice(0, 1);
          document.labels_distribution.forEach(
            (label: { label: string; percentage: number }, i: number) => {
              addLabel(lastDataIndex);
              form.value.data[lastDataIndex].labels[i].description =
                label.label;
              form.value.data[lastDataIndex].labels[i].percentage =
                label.percentage;
            },
          );

          form.value.data[lastDataIndex].rights = document.data_rights;
          form.value.data[lastDataIndex].policies = document.data_policies;

          form.value.data[lastDataIndex].fields.splice(0, 1);
          document.fields.forEach(
            (
              fields: {
                field_name: string;
                field_description: string;
                field_type: string;
                expected_values: string;
                interpret_missing: string;
                interpret_special: string;
              },
              i: number,
            ) => {
              addField(lastDataIndex);
              form.value.data[lastDataIndex].fields[i].name = fields.field_name;
              form.value.data[lastDataIndex].fields[i].description =
                fields.field_description;
              form.value.data[lastDataIndex].fields[i].type = fields.field_type;
              form.value.data[lastDataIndex].fields[i].expected_values =
                fields.expected_values;
              form.value.data[lastDataIndex].fields[i].missing_values =
                fields.interpret_missing;
              form.value.data[lastDataIndex].fields[i].special_values =
                fields.interpret_special;
            },
          );
        } else if (descriptorName === "Development Environment") {
          form.value.model.development.resources.gpu =
            document.computing_resources.gpu;
          form.value.model.development.resources.cpu =
            document.computing_resources.cpu;
          form.value.model.development.resources.memory =
            document.computing_resources.memory;
          form.value.model.development.resources.storage =
            document.computing_resources.storage;

          let outputString = "";
          if (form.value.model.production.interface.output.description !== "") {
            outputString += "\n\n";
          }
          document.downstream_components.forEach(
            (component: {
              component_name: string;
              input_spec: [
                {
                  item_name: string;
                  item_description: string;
                  item_type: string;
                  expected_values: string;
                },
              ];
              ml_component: boolean;
            }) => {
              outputString +=
                "Component Name: " + component.component_name + "\n";
              outputString += "ML Component: " + component.ml_component + "\n";
              component.input_spec.forEach(
                (spec: {
                  item_name: string;
                  item_description: string;
                  item_type: string;
                  expected_values: string;
                }) => {
                  outputString += spec.item_name + "\n";
                  outputString += spec.item_description + "\n";
                  outputString += spec.item_type + "\n";
                  outputString += spec.expected_values + "\n";
                },
              );
              outputString += "\n";
            },
          );
          outputString = outputString.substring(0, outputString.length - 2);
          form.value.model.production.interface.output.description +=
            outputString;
        } else if (descriptorName === "Production Environment") {
          form.value.model.production.resources.gpu =
            document.computing_resources.gpu;
          form.value.model.production.resources.cpu =
            document.computing_resources.cpu;
          form.value.model.production.resources.memory =
            document.computing_resources.memory;
          form.value.model.production.resources.storage =
            document.computing_resources.storage;
        }
      } catch (err) {
        console.error("Invalid JSON or error in parsing file.");
      }
    };
    reader.readAsText(file);
  }
}

function addGoal() {
  form.value.system.goals.push({
    description: "",
    metrics: [{ description: "", baseline: "" }],
  });
}

function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    form.value.system.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex: number) {
  form.value.system.goals[goalIndex].metrics.push({
    description: "",
    baseline: "",
  });
}

function deleteMetric(goalIndex: number, metricIndex: number) {
  if (confirm("Are you sure you want to delete this metric?")) {
    form.value.system.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}

function addDataItem() {
  form.value.data.push({
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
    form.value.data.splice(dataItemIndex, 1);
  }
}

function addLabel(dataItemIndex: number) {
  form.value.data[dataItemIndex].labels.push({
    name: "",
    description: "",
    percentage: 0,
  });
}

function deleteLabel(dataItemIndex: number, labelIndex: number) {
  if (confirm("Are you sure you want to delete this label?")) {
    form.value.data[dataItemIndex].labels.splice(labelIndex, 1);
  }
}

function addField(dataItemIndex: number) {
  form.value.data[dataItemIndex].fields.push({
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
    form.value.data[dataItemIndex].fields.splice(fieldIndex, 1);
  }
}

function addRequirement() {
  form.value.system_requirements.push({
    quality: "<System Quality>",
    stimulus: "<Stimulus>",
    source: "<Source>",
    environment: "<Environment>",
    response: "<Response>",
    measure: "<Response Measure>",
  });
}

function deleteRequirement(requirementIndex: number) {
  if (confirm("Are you sure you want to delete this requirement?")) {
    form.value.system_requirements.splice(requirementIndex, 1);
  }
}

</script>


