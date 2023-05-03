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
      <div v-for="(goal, index) in form.system.goals">
        <p><b>Goal {{ index + 1 }}</b></p>

        <UsaTextInput v-model="goal.description">
          <template v-slot:label>
            Goals of the system <img src="~/assets/uswds/img/usa-icons/info.svg"/>
          </template>
        </UsaTextInput>

        <div v-for="(metric, index) in goal.metrics">
          <UsaTextInput v-model="metric.description">
            <template v-slot:label>
              Metric subfield description @@ TODO: Update this label when list structure changes @@
            </template>
          </UsaTextInput>

          <UsaTextInput v-model="metric.baseline">
            <template v-slot:label>
              Baseline
            </template>
          </UsaTextInput>
        </div>
        <hr/>
      </div>

      <button @click="addGoal" class="usa button usa-button--unstyled">
        <img src="~/assets/uswds/img/usa-icons/add_circle.svg"/> Add more goal(s)
      </button>
    </div>

    <UsaTextInput v-model="form.system.problem_type">
      <template v-slot:label>
        ML Problem Type <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.task">
      <template v-slot:label>
        ML Task <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.usage_context">
      <template v-slot:label>
        Usage Context <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.fp_risk">
      <template v-slot:label>
        False Positive Risk <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.system.fn_risk">
      <template v-slot:label>
        False Negative Risk <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.other_risks">
      <template v-slot:label>
        Other risks of producing incorrect results <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <hr/>

    <h3 class="section-header">Data</h3>
    <UsaTextInput v-model="form.data.source_data_location">
      <template v-slot:label>
        Source Data Location <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>
    
    <UsaTextInput v-model="form.data.data_classification">
      <template v-slot:label>
        Data Classification <img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.data.account_access">
      <template v-slot:label>
        Account Access / Account Availability<img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <UsaTextInput >
      <template v-slot:label>
        Labels / Distribution @@ TODO PLACEHOLDER @@<img src="~/assets/uswds/img/usa-icons/info.svg"/>
      </template>
    </UsaTextInput>

    <button class="usa-button usa-button--unstyled">
      <img src="~/assets/uswds/img/usa-icons/add_circle.svg"/>Add Additional Labels
    </button>

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

      <button @click="addSchema" class="usa-button usa-button--unstyled">
        <img src="~/assets/uswds/img/usa-icons/add_circle.svg"/>Add additional field(s)
      </button>
    </div>

    <UsaTextarea v-model="form.data_rights">
      <template v-slot:label>
        Data Rights
      </template>
    </UsaTextarea>

    <UsaTextarea v-model="form.data_policies">
      <template v-slot:label>
        Data Policies
      </template>
    </UsaTextarea>

    <hr/>
    
    <h3 class="section-header">Model</h3>
    <div class="input-group" style="margin-top: 1em;">
      <h3 class="section-header">Development Compute Resources</h3>
      <div style="display: inline-block; border: 1px solid red; width: 40%">
        <UsaTextInput v-model="form.model.development.resources.gpus" type="number">
          <template v-slot:label>
            Graphics Processing Units (GPUs)
          </template>
        </UsaTextInput>
      </div>

      <div style="display: inline-block; border: 1px solid green; width: 40%">
        <UsaTextInput v-model="form.model.development.resources.cpus" type="number">
          <template v-slot:label>
            Central Processing Units (CPUs)
          </template>
        </UsaTextInput>
      </div>

      <UsaTextInput v-model="form.model.development.resources.memory" type="number">
        <template v-slot:label>
          Memory
        </template>
        <template v-slot:input-suffix>
          GB
        </template>
      </UsaTextInput>

      <UsaTextInput v-model="form.model.development.resources.storage" type="number">
        <template v-slot:label>
          Storage
        </template>
        <template v-slot:input-suffix>
          GB
        </template>
      </UsaTextInput>
    </div>

    <UsaTextInput v-model="form.model.production.environment.integration">
      <template v-slot:label>
        Integration
      </template>
    </UsaTextInput>

    <UsaTextInput v-model="form.model.production.environment.output">
      <template v-slot:label>
        Output
      </template>
    </UsaTextInput>

    <div class="input-group" style="margin-top: 1em;">
      <h3 class="section-header">Production Compute Resources</h3>
      <div style="display: inline-block; border: 1px solid red; width: 40%">
        <UsaTextInput v-model="form.model.production.resources.gpus" type="number">
          <template v-slot:label>
            Graphics Processing Units (GPUs)
          </template>
        </UsaTextInput>
      </div>

      <div style="display: inline-block; border: 1px solid green; width: 40%">
        <UsaTextInput v-model="form.model.production.resources.cpus" type="number">
          <template v-slot:label>
            Central Processing Units (CPUs)
          </template>
        </UsaTextInput>
      </div>

      <UsaTextInput v-model="form.model.production.resources.memory" type="number">
        <template v-slot:label>
          Memory
        </template>
        <template v-slot:input-suffix>
          GB
        </template>
      </UsaTextInput>

      <UsaTextInput v-model="form.model.production.resources.storage" type="number">
        <template v-slot:label>
          Storage
        </template>
        <template v-slot:input-suffix>
          GB
        </template>
      </UsaTextInput>
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