<template>
  <NuxtLayout name="base-layout">
    <UsaBreadcrumb :items="path"/>

    <h2 class="section-header">How to use Negotiation Card</h2>
    <p>
      Teams should work through as many of the following items as they can at the IMT negotiation point, using
      the answers to inform initial model development. At the SDMT negotiation point, answers should be
      modified/updated according to the results of IMT. As the <a href="/TODO">Specification</a> is created,
      teams should refer to this negotiation card to ensure they capture all relevant critical aspects
      of the model and system.
    </p>

    <h3 class="section-header">System Requirements</h3>
    <div class="input-group">
      <h3 class="section-header">Goals</h3>
      <p>
        Goals or objectives that the model is going to help satisfy.
      </p>
      <div v-for="(goal, goalIndex) in form.system.goals">
        <p><b>Goal {{ goalIndex + 1 }}</b></p>

        <UsaTextInput v-model="goal.description">
          <template v-slot:label>
            Goal Description
          </template>
        </UsaTextInput>

        <div v-for="(metric, index) in goal.metrics">
          <UsaTextInput v-model="metric.description">
            <template v-slot:label>
              Metric subfield description @@ TODO: Update this label when list structure changes @@@
              <InfoIcon>
                For each goal, select a performance metric that captures the system's 
                ability to accomplish that goal; e.g., acceptance criteria for determining
                that the model is performing correctly.
              </InfoIcon>
            </template>
          </UsaTextInput>

          <UsaTextInput v-model="metric.baseline">
            <template v-slot:label>
              Baseline
              <InfoIcon>
                Select a baseline for each performance metric, which means a measurement that 
                evaluates whether or not the model will/can achieve the main goal for which it is being created. 
                If the goal cannot be measured directly, select a reasonable proxy and justify how that will 
                reliably predict the model’s performance in achieving its goal.
              </InfoIcon>
            </template>
          </UsaTextInput>
        </div>
        <DeleteButton @click="deleteGoal(goalIndex)">
          Delete goal
        </DeleteButton>
        <hr/>
      </div>

      <AddButton @click="addGoal()">
        Add goal
      </AddButton>
    </div>

    <UsaTextInput v-model="form.system.problem_type">
      <template v-slot:label>
        ML Problem Type
        <InfoIcon>
          Type of ML problem that the model is intended to solve.
        </InfoIcon>
      </template>
    </UsaTextInput>

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

    <hr/>

    <h3 class="section-header">Data</h3>
    <p>
      Details of the data that will influence development efforts; fill out all that are known. For 
      access / availability, record what needs to happen to access the data, such as accounts that 
      need to be created or methods for data transportation.
    </p>
    <UsaTextInput v-model="form.data.source_data_location">
      <template v-slot:label>
        Source Data Location
      </template>
    </UsaTextInput>
    
    <UsaTextInput v-model="form.data.data_classification">
      <template v-slot:label>
        Data Classification
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.data.account_access">
      <template v-slot:label>
        Account Access / Account Availability
      </template>
    </UsaTextInput>

    <UsaTextInput >
      <template v-slot:label>
        Labels / Distribution @@ TODO PLACEHOLDER @@<img src="~/assets/uswds/img/usa-icons/info.svg" class="inline-icon"/>
      </template>
    </UsaTextInput>

    <AddButton>
      Add additional labels
    </AddButton>

    <hr/>

    <div class="input-div">
      <h3>Data Schema</h3>
      <div v-for="(schema, index) in form.data_schema" :key="index">
        <UsaTextInput v-model="schema.field_name">
          <template v-slot:label>
            Field Name
          </template>
        </UsaTextInput>

        <UsaTextarea v-model="schema.field_description">
          <template v-slot:label>
            Field Description
          </template>
        </UsaTextarea>

        <UsaTextInput v-model="schema.field_type">
          <template v-slot:label>
            Field Type
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="schema.expected_values">
          <template v-slot:label>
            Expected Values
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="schema.missing_values">
          <template v-slot:label>
            Missing Values
          </template>
        </UsaTextInput>

        <UsaTextInput v-model="schema.special_values">
          <template v-slot:label>
            Special Values
          </template>
        </UsaTextInput>
        <hr/>
      </div>

      <AddButton @click="addSchema()">
        Add additional field(s)
      </AddButton>
    </div>

    <UsaTextarea v-model="form.data_rights">
      <template v-slot:label>
        Data Rights
        <InfoIcon>
          Are there particular ways in which the data can and cannot be used?
        </InfoIcon>
      </template>
    </UsaTextarea>

    <UsaTextarea v-model="form.data_policies">
      <template v-slot:label>
        Data Policies
        <InfoIcon>
          Are there policies that govern the data and its use, such as Personally Identifiable 
          Information [PII]?
        </InfoIcon>
      </template>
    </UsaTextarea>

    <hr/>
    
    <h3 class="section-header">Model</h3>
    <div class="input-group" style="margin-top: 1em;">
      <h3 class="section-header">Development Compute Resources</h3>
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
      <h3 class="section-header">Production Compute Resources</h3>
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

    <hr/>

    <div style="text-align: right;">
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
    data: {
      source_data_location: "",
      data_classification: "",
      account_access: "",
      labels: [
        {
          identifier: "",
          distribution: "",
        }
      ],
    },
    data_schema: [
      {
        field_name: "",
        field_description: "",
        field_type: "",
        expected_values: "",
        missing_values: "",
        special_values: ""
      }
    ],
    data_rights: "",
    data_policies: "",
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


  function printState(){
    console.log(form.value)
  }

  function addGoal(){
    form.value.system.goals.push({"description": "", "metrics": [{"performance_metrics": "", "baseline": ""}]})
  }

  function deleteGoal(index){
    form.value.system.goals.splice(index, 1);
  }

  function addSchema(){
    form.value.data_schema.push({"field_name": "", "field_description": "", "field_type": "", "expected_values": "",
                                  "missing_values": "", "special_values": ""})
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