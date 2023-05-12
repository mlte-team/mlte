<template>
  <NuxtLayout name="base-layout">
    <UsaBreadcrumb :items="path"/>

    <h1 class="section-header">How to use Negotiation Card</h1>
    <p>
      Teams should work through as many of the following items as they can at the IMT negotiation point, using
      the answers to inform initial model development. At the SDMT negotiation point, answers should be
      modified/updated according to the results of IMT. As the <a href="/TODO">Specification</a> is created,
      teams should refer to this negotiation card to ensure they capture all relevant critical aspects
      of the model and system.
    </p>

    <h2 class="section-header">System Requirements</h2>
    <div class="input-group">
      <h3>Goals</h3>
      <p>
        Goals or objectives that the model is going to help satisfy.
      </p>
      <div v-for="(goal, goal_index) in form.system.goals">
        <p><b>Goal {{ goal_index + 1 }}</b></p>

        <UsaTextInput v-model="goal.description">
          <template v-slot:label>
            Goal Description
          </template>
        </UsaTextInput>

        <h3 class="no-margin-section-header">Metrics</h3>
        <div v-for="(metric, metric_index) in goal.metrics">
          <div class="inline-input-left">
            <UsaTextInput v-model="metric.description">
              <template v-slot:label>
                Description
                <InfoIcon>
                  For each goal, select a performance metric that captures the system's 
                  ability to accomplish that goal; e.g., acceptance criteria for determining
                  that the model is performing correctly.
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>

          <div class="inline-input-right">
            <UsaTextInput v-model="metric.baseline">
              <template v-slot:label>
                Baseline
                <InfoIcon>
                  Select a baseline for each performance metric, which means a measurement that <br/>
                  evaluates whether or not the model will/can achieve the main goal for which it is being created. <br/>
                  If the goal cannot be measured directly, select a reasonable proxy and justify how that will <br/>
                  reliably predict the model’s performance in achieving its goal.
                </InfoIcon>
              </template>
            </UsaTextInput>
          </div>
          <div class="inline-button">
            <DeleteButton @click="deleteMetric(goal_index, metric_index)">
              Delete Metric
            </DeleteButton>
          </div>
        </div>
        <AddButton @click="addMetric(goal_index)" class="margin-button">
          Add Metric
        </AddButton>
        <DeleteButton @click="deleteGoal(goal_index)">
          Delete goal
        </DeleteButton>
        <hr/>
      </div>

      <AddButton @click="addGoal()" class="margin-button">
        Add goal
      </AddButton>
    </div>

    <UsaSelect v-model="form.system.problem_type" :options=problem_type_options>
      <template v-slot:label>
        ML Problem Type
        <InfoIcon>
          Type of ML problem that the model is intended to solve.
        </InfoIcon>
      </template>
    </UsaSelect>

    <UsaTextInput v-model="form.system.task">
      <template v-slot:label>
        ML Task
        <InfoIcon>
          Well-defined task that model is expected to perform, or problem that the model is 
          expected to solve.
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.usage_context">
      <template v-slot:label>
        Usage Context
        <InfoIcon>
          Who is intended to utilize the system/model; how the results of the model are 
          going to be used by end users or in the context of a larger system.
        </InfoIcon>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.fp_risk">
      <template v-slot:label>
        False Positive Risk
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.fn_risk">
      <template v-slot:label>
        False Negative Risk
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.other_risks">
      <template v-slot:label>
        Other risks of producing incorrect results
      </template>
    </UsaTextInput>

    <h2 class="section-header">Data</h2>
    <p>
      Details of the data that will influence development efforts; fill out all that are known. For 
      access / availability, record what needs to happen to access the data, such as accounts that 
      need to be created or methods for data transportation.
    </p>
    <div class="input-group">
      <div v-for="(data_item, data_item_index) in form.data">
        <h3>Data Item {{ data_item_index + 1 }}</h3>
        <UsaTextInput v-model="data_item.access">
          <template v-slot:label>
            Account Access / Account Availability
          </template>
        </UsaTextInput>

        <div>
          <div class="inline-input-left">
            <UsaTextInput v-model="data_item.description">
              <template v-slot:label>
                Data Description
              </template>
            </UsaTextInput>
          </div>
          
          <div class="inline-input-right">
            <UsaTextInput v-model="data_item.source">
              <template v-slot:label>
                Source Data Location
              </template>
            </UsaTextInput>
          </div>
        </div>

        <UsaSelect v-model="data_item.classification" :options=classiciation_options>
          <template v-slot:label>
            Data Classification
          </template>
        </UsaSelect>

        <div class="input-group" style="margin-top: 1em;">
          <div v-for="(label, label_index) in data_item.labels">
            <div class="inline-input-left">
              <UsaTextInput v-model="label.description">
                <template v-slot:label>
                  Label Description
                </template>
              </UsaTextInput>
            </div>

            <div class="inline-input-right">
              <UsaTextInput v-model="label.percentage" type="number">
                <template v-slot:label>
                  Percentage
                </template>
              </UsaTextInput>
            </div>
            <div class="inline-button">
              <DeleteButton @click="deleteLabel(data_item_index, label_index)">
                Delete label
              </DeleteButton>
            </div>
          </div>

          <AddButton @click="addLabel(data_item_index)" class="margin-button">
            Add additional label
          </AddButton>
        </div>

        <div class="input-group" style="margin-top: 1em;">
          <h3 class="no-margin-section-header">Data Schema</h3>
          <div v-for="(field, field_index) in data_item.schema">
            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="field.name">
                  <template v-slot:label>
                    Field Name
                  </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="field.description">
                  <template v-slot:label>
                    Field Description
                  </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="field.type">
                  <template v-slot:label>
                    Field Type
                  </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="field.expected_values">
                  <template v-slot:label>
                    Expected Values
                  </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="field.missing_values">
                  <template v-slot:label>
                    Missing Values
                  </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="field.special_values">
                  <template v-slot:label>
                    Special Values
                  </template>
                </UsaTextInput>
              </div>
            </div>
            <DeleteButton @click="deleteField(data_item_index, field_index)" class="margin-button">
              Delete field
            </DeleteButton>
            <hr/>
          </div>

          <AddButton @click="addField(data_item_index)" class="margin-button">
            Add additional field
          </AddButton>
        </div>

        <UsaTextInput v-model="data_item.rights">
          <template v-slot:label>
            Data Rights
            <InfoIcon>
              Are there particular ways in which the data can and cannot be used?
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="data_item.policies">
          <template v-slot:label>
            Data Policies
            <InfoIcon>
              Are there policies that govern the data and its use, such as Personally Identifiable 
              Information [PII]?
            </InfoIcon>
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="data_item.identifiable_information">
          <template v-slot:label>
            Identifiable Information
          </template>
        </UsaTextInput>

        <DeleteButton @click="deleteDataItem(data_item_index)" class="margin-button">
          Delete data item
        </DeleteButton>
        <hr/>
      </div>
      <AddButton @click="addDataItem()" class="margin-button">
        Add data item
      </AddButton>
    </div>

    <h2 class="section-header">Model</h2>
    <div class="input-group">
      <h3>Development Compute Resources</h3>
      <p>
        Describe the amount and type of compute resources 
        needed for training.
      </p>
      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.development.resources.gpus" type="number">
            <template v-slot:label>
              Graphics Processing Units (GPUs)
            </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.development.resources.cpus" type="number">
            <template v-slot:label>
              Central Processing Units (CPUs)
            </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.development.resources.memory" type="number">
            <template v-slot:label>
              Memory
            </template>
            <template v-slot:input-suffix>
              GB
            </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.development.resources.storage" type="number">
            <template v-slot:label>
              Storage
            </template>
            <template v-slot:input-suffix>
              GB
            </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <UsaTextarea v-model="form.model.production.environment.integration">
      <template v-slot:label>
        Integration
        <InfoIcon>
          Describe how the model will be integrated into the system; this likely 
          includes descriptions of model deployment, application hosting, etc.
        </InfoIcon>
      </template>
    </UsaTextarea>

    <UsaTextInput v-model="form.model.production.environment.output">
      <template v-slot:label>
        Output
        <InfoIcon>
          Describe the output format and specification needed for the system to 
          ingest model results.
        </InfoIcon>
      </template>
    </UsaTextInput>

    <div class="input-group" style="margin-top: 1em;">
      <h3>Production Compute Resources</h3>
      <p>
        Describe the hardware and software requirements including amount of
        compute resources needed for inference.
      </p>
      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.production.resources.gpus" type="number">
            <template v-slot:label>
              Graphics Processing Units (GPUs)
            </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.production.resources.cpus" type="number">
            <template v-slot:label>
              Central Processing Units (CPUs)
            </template>
          </UsaTextInput>
        </div>
      </div>

      <div>
        <div class="inline-input-left">
          <UsaTextInput v-model="form.model.production.resources.memory" type="number">
            <template v-slot:label>
              Memory
            </template>
            <template v-slot:input-suffix>
              GB
            </template>
          </UsaTextInput>
        </div>

        <div class="inline-input-right">
          <UsaTextInput v-model="form.model.production.resources.storage" type="number">
            <template v-slot:label>
              Storage
            </template>
            <template v-slot:input-suffix>
              GB
            </template>
          </UsaTextInput>
        </div>
      </div>
    </div>

    <div style="text-align: right; margin-top: 1em;">
      <button @click="cancel" class="usa-button cancel-button">
        Cancel
      </button>
      <button @click="printState" class="usa-button save-button">
        Save
      </button>
    </div>

  </NuxtLayout>
</template>

<script setup>
  var path = ref([
    {
      "to": "/",
      "text": "Artifact Store"
    },
    {
      "to": "/negotiation-store",
      "text": "Negotiation Card"
    }
  ])

  var form = ref({
    system: {
      goals: [{
        description: "",
        metrics: [{
          description: "",
          baseline: ""
        }]
      }],
      problem_type: "",
      task: "",
      usage_context: "",
      fp_risk: "",
      fn_risk: "",
      other_risks: "",
    },
    data: [
      {
        access: "",
        description: "",
        source: "",
        classification: "",
        labels: [
          {
            description: "",
            percentage: 0,
          }
        ],
        schema: [
          {
            name: "",
            description: "",
            type: "",
            expected_values: "",
            missing_values: "",
            special_values: "",
          }
        ],
        rights: "",
        policies: "",
        identifiable_information: ""
      }
    ],
    model: {
      development: {
        resources: {
          gpus: 0,
          cpus: 0,
          memory: 0,
          storage: 0
        }
      },
      production: {
        environment: {
          integration: "",
          output: "",
        },
        resources: {
          gpus: 0,
          cpus: 0,
          memory: 0,
          storage: 0
        }
      }
    }
  })

  var problem_type_options = ([
    {"value": "Classification", "text": "Classification"},
    {"value": "Clustering", "text": "Clustering"},
    {"value": "Content Generation", "text": "Content Generation"},
    {"value": "Detection", "text": "Detection"},
    {"value": "Trend", "text": "Trend"},
    {"value": "Alert", "text": "Alert"},
    {"value": "Forecasting", "text": "Forecasting"},
    {"value": "Summarization", "text": "Summarization"},
    {"value": "Benchmarking", "text": "Benchmarking"},
    {"value": "Goals", "text": "Goals"},
    {"value": "Other", "text": "Other"},
  ])

  var classiciation_options = ([
    {"value": "Unclassified", "text": "Unclassified"},
    {"value": "Controlled Unclassified Information (CUI)", "text": "Controlled Unclassified Information (CUI)"},
    {"value": "Personally Identifiable Information (PII)", "text": "Personally Identifiable Information (PII)"},
    {"value": "Protected Health Information (PHI)", "text": "Protected Health Information (PHI)"},
    {"value": "Other", "text": "Other"},
  ])


  function printState(){
    console.log(form.value)
  }

  function addGoal(){
    form.value.system.goals.push({"description": "", "metrics": [{"performance_metrics": "", "baseline": ""}]})
  }

  function deleteGoal(goal_index){
    form.value.system.goals.splice(goal_index, 1);
  }

  function addMetric(goal_index){
    form.value.system.goals[goal_index].metrics.push({"description": "", "baseline": ""})
  }

  function deleteMetric(goal_index, metric_index){
    form.value.system.goals[goal_index].metrics.splice(metric_index, 1)
  }

  function addDataItem(){
    form.value.data.push(
      {
        access: "",
        description: "",
        source: "",
        classification: "",
        labels: [
          {
            description: "",
            percentage: 0,
          }
        ],
        schema: [
          {
            name: "",
            description: "",
            type: "",
            expected_values: "",
            missing_values: "",
            special_values: "",
          }
        ],
        rights: "",
        policies: "",
        identifiable_information: ""
      }
    )
  }

  function deleteDataItem(data_item_index){
    form.value.data.splice(data_item_index, 1)
  }

  function addLabel(data_item_index){
    form.value.data[data_item_index].labels.push({"description": "", "percentage": 0})
  }

  function deleteLabel(data_item_index, label_index){
    form.value.data[data_item_index].labels.splice(label_index, 1)
  }

  function addField(data_item_index){
    form.value.data[data_item_index].schema.push(
      {
        "name": "",
        "description": "", 
        "type": "",
        "expected_values": "",
        "missing_values": "",
        "special_values": ""
      }
    )
  }

  function deleteField(data_item_index, field_index){
    form.value.data[data_item_index].schema.splice(field_index, 1)
  }

</script>

<style>
.cancel-button {
  background-color: transparent;
  box-shadow: inset 0 0 0 2px #d8ac16;
  color: black;
}

.save-button {
  background-color: #d8ac16;
  color: black;
}
</style>