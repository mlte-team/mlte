<template>
  <NuxtLayout name="base-layout">
    <template v-slot:sidebar>
      TEC Import
      <hr/>
      <div class="usa-form-group">
        <label class="usa-label">
          System Context
        </label>
        <input class="usa-file-input" type="file" accept=".json" @change="descriptorUpload('System Context')"/>

        <label class="usa-label">
          Raw Data
        </label>
        <input class="usa-file-input" type="file" accept=".json" @change="descriptorUpload('Raw Data')"/>

        <label class="usa-label">
          Development Environment
        </label>
        <input class="usa-file-input" type="file" accept=".json" @change="descriptorUpload('Development Environment')"/>

        <label class="usa-label">
          Production Environment
        </label>
        <input class="usa-file-input" type="file" accept=".json" @change="descriptorUpload('Production Environment')"/>
      </div>
    </template>

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
        <h3>Goal {{ goal_index + 1 }}</h3>

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

    <UsaTextInput v-model="form.system.other_risks">
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

        <UsaSelect v-model="data_item.classification" :options=classification_options>
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
          <div v-for="(schema, schema_index) in data_item.schema">
          <h3 class="no-margin-section-header">Data Schema {{ data_item_index + 1 }} - {{ schema_index + 1 }}</h3>
            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="schema.name">
                  <template v-slot:label>
                    Field Name
                  </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="schema.description">
                  <template v-slot:label>
                    Field Description
                  </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="schema.type">
                  <template v-slot:label>
                    Field Type
                  </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="schema.expected_values">
                  <template v-slot:label>
                    Expected Values
                  </template>
                </UsaTextInput>
              </div>
            </div>

            <div>
              <div class="inline-input-left">
                <UsaTextInput v-model="schema.missing_values">
                  <template v-slot:label>
                    Missing Values
                  </template>
                </UsaTextInput>
              </div>

              <div class="inline-input-right">
                <UsaTextInput v-model="schema.special_values">
                  <template v-slot:label>
                    Special Values
                  </template>
                </UsaTextInput>
              </div>
            </div>
            <DeleteButton @click="deleteSchema(data_item_index, schema_index)" class="margin-button">
              Delete schema
            </DeleteButton>
            <hr/>
          </div>

          <AddButton @click="addSchema(data_item_index)" class="margin-button">
            Add additional schema
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

    <UsaTextarea v-model="form.model.production.environment.output">
      <template v-slot:label>
        Output
        <InfoIcon>
          Describe the output format and specification needed for the system to 
          ingest model results.
        </InfoIcon>
      </template>
    </UsaTextarea>

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
      <UsaButton @click="cancel()" class="secondary-button">
        Cancel
      </UsaButton>
      <UsaButton @click="submit()" class="primary-button">
        Save
      </UsaButton>
    </div>

  </NuxtLayout>
</template>

<script setup>
  var path = ref([
    {
      "href": "/",
      "text": "Artifact Store"
    },
    {
      "href": "/negotiation-store",
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

  var classification_options = ([
    {"value": "Unclassified", "text": "Unclassified"},
    {"value": "Controlled Unclassified Information (CUI)", "text": "Controlled Unclassified Information (CUI)"},
    {"value": "Personally Identifiable Information (PII)", "text": "Personally Identifiable Information (PII)"},
    {"value": "Protected Health Information (PHI)", "text": "Protected Health Information (PHI)"},
    {"value": "Other", "text": "Other"},
  ])


  function submit(){
    console.log(form.value)
    console.log(useRoute().query.namespace)
  }

  function descriptorUpload(descriptor_name){
    if(event.target.files[0]){
      var file = event.target.files[0]
      const reader = new FileReader();
      reader.onload = (res) => {
        try{
          var document = JSON.parse(res.target.result);
        }
        catch(err){
          console.error("Invalid JSON")
          return;
        }
        if(descriptor_name == "System Context"){
          document.goals.forEach((goal, i) => {
            addGoal();
            var last_goal_index = form.value.system.goals.length - 1;

            form.value.system.goals[last_goal_index].description = goal.goal;
            form.value.system.goals[last_goal_index].metrics[0].description = goal.metric;
            form.value.system.goals[last_goal_index].metrics[0].baseline = goal.baseline;
          })
          form.value.system.task = document.task;
          form.value.system.problem_type = document.ml_problem_type.ml_problem;
          form.value.system.usage_context = document.usage_context;
          form.value.system.fp_risk = document.risks.risk_fp;
          form.value.system.fn_risk = document.risks.risk_fn;
          form.value.system.other_risks = document.risks.risk_other;
        }
        else if(descriptor_name == "Raw Data"){
          addDataItem();
          var last_data_index = form.value.data.length - 1;

          var data_sources_str = "";
          document.data_sources.forEach((source, i) => {
            if(source.data_source == "Other"){
              data_sources_str += source.other_source;
            }
            else{
              data_sources_str += source.data_source;
            }

            if(i + 1 < document.data_sources.length){
              data_sources_str += ", "
            }
          })
          form.value.data[last_data_index].source = data_sources_str;

          form.value.data[last_data_index].labels.splice(0, 1)
          document.labels_distribution.forEach((label, i) => {
            addLabel(last_data_index);
            form.value.data[last_data_index].labels[i].description = label.label;
            form.value.data[last_data_index].labels[i].percentage = label.percentage;
          })

          form.value.data[last_data_index].rights = document.data_rights;
          form.value.data[last_data_index].policies = document.data_policies;

          form.value.data[last_data_index].schema.splice(0, 1);
          document.schema.forEach((schema, i) => {
            addSchema(last_data_index);
            form.value.data[last_data_index].schema[i].name = schema.field_name;
            form.value.data[last_data_index].schema[i].description = schema.field_description;
            form.value.data[last_data_index].schema[i].type = schema.field_type;
            form.value.data[last_data_index].schema[i].expected_values = schema.expected_values;
            form.value.data[last_data_index].schema[i].missing_values = schema.interpret_missing;
            form.value.data[last_data_index].schema[i].special_values = schema.interpret_special;
          })
        }
        else if(descriptor_name == "Development Environment"){
          form.value.model.development.resources.gpus = document.computing_resources.gpu;
          form.value.model.development.resources.cpus = document.computing_resources.cpu;
          form.value.model.development.resources.memory = document.computing_resources.memory;
          form.value.model.development.resources.storage = document.computing_resources.storage;

          var output_string = "";
          if(form.value.model.production.environment.output != ""){
            output_string += "\n\n"
          }
          document.downstream_components.forEach((component, i) => {
            output_string += "Component Name: " + component.component_name + "\n";
            output_string += "ML Component: " + component.ml_component + "\n"
            component.input_spec.forEach((spec, j) => {
              output_string += spec.item_name + "\n"
              output_string += spec.item_description + "\n"
              output_string += spec.item_type + "\n"
              output_string += spec.expected_values + "\n"
            })
            output_string += "\n"
          })
          output_string = output_string.substring(0, output_string.length - 2)
          form.value.model.production.environment.output += output_string;
        }
        else if(descriptor_name == "Production Environment"){
          form.value.model.production.resources.gpus = document.computing_resources.gpu;
          form.value.model.production.resources.cpus = document.computing_resources.cpu;
          form.value.model.production.resources.memory = document.computing_resources.memory;
          form.value.model.production.resources.storage = document.computing_resources.storage;
        }
      }
      reader.readAsText(file);
    }
  }

  function addGoal(){
    form.value.system.goals.push({"description": "", "metrics": [{"performance_metrics": "", "baseline": ""}]})
  }

  function deleteGoal(goal_index){
    if(confirm("Are you sure you want to delete this goal?")){
      form.value.system.goals.splice(goal_index, 1);
    }
  }

  function addMetric(goal_index){
    form.value.system.goals[goal_index].metrics.push({"description": "", "baseline": ""})
  }

  function deleteMetric(goal_index, metric_index){
    if(confirm("Are you sure you want to delete this metric?")){
      form.value.system.goals[goal_index].metrics.splice(metric_index, 1)
    }
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
    if(confirm("Are you sure you want to delete this data item?")){
      form.value.data.splice(data_item_index, 1)
    }
  }

  function addLabel(data_item_index){
    form.value.data[data_item_index].labels.push({"description": "", "percentage": 0})
  }

  function deleteLabel(data_item_index, label_index){
    if(confirm("Are you sure you want to delete this label?")){
      form.value.data[data_item_index].labels.splice(label_index, 1)
    }
  }

  function addSchema(data_item_index){
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

  function deleteSchema(data_item_index, field_index){
    if(confirm("Are you sure you want to delete this field?")){
      form.value.data[data_item_index].schema.splice(field_index, 1)
    }
  }
</script>

<style>
.sidebar {
  padding-top: 255px;
}
</style>