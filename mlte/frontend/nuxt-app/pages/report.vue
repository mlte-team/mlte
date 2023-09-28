<template>
  <NuxtLayout name="base-layout">
    
    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">MLTE REPORT</h1>

    <h3>Model Summary</h3>
    <UsaTextarea>
      <template #label>
        Summary of the model being evaluated.
      </template>
          <!-- Note that when I type in this text box, 
            it clicks out of the area every time I type a letter.
          The same thing happens in the negotiation card
          in a few of the text boxes, so we need to fix that. -->
    </UsaTextarea>

    <!-- Kept the goals section consistent from what Alex had.
    Probably need to rewrite once we figure out how to pull 
    sections from the negotiation card.-->
    <h3>Goals of the System</h3>
      <p>Goals or objectives that the model helps to satisfy.</p>
      <div
        v-for="(goal, goalIndex) in form.goals"
        :key="goal.description"
      >
        <h3>Goal {{ goalIndex + 1 }}</h3>

        <UsaTextInput v-model="goal.description">
          <template #label> Goal Description </template>
        </UsaTextInput>

      </div>
      <AddButton class="margin-button" @click="addGoal()"> Add goal </AddButton>
      <!-- For some reason I cannot get this button to work properly
        <DeleteButton @click="deleteGoal(goalIndex)">
          Delete goal
        </DeleteButton> 
      -->
    <h3>MLTE Evaluation</h3>
      <p>THIS IS A PLACEHOLDER
        <br />
        <br />
        <br />
        TO DELINEATE A SPACE
        <br />
        <br />
        <br />
        WHERE MLTE EVALUATION RESULTS
        <br />
        <br />
        <br />
        WILL EVENTUALLY LIVE.
        <br />
        <br />
        <br />
      </p>
    
    <h3>Intended Use</h3>
    <UsaTextarea>
      <template #label>
        Description of how the model is intended to be used.
      </template>
    </UsaTextarea>

    <h3>Risks</h3>
    <UsaTextarea>
      <template #label>
        Description of model and system risks.
      </template>
    </UsaTextarea>

    <h3>Data</h3>
    <UsaTextarea>
      <template #label>
        Description of data used to train the model.
      </template>
    </UsaTextarea>

    <h3>Caveats and Recommendations</h3>
    <UsaTextarea>
      <template #label>
        Description of any caveats and recommendations for the system or model.
      </template>
    </UsaTextarea>

    <h3>Quantitative Analysis</h3>
      <p>THIS IS A PLACEHOLDER
        <br />
        <br />
        <br />
        TO REPRESENT THE SPACE
        <br />
        <br />
        <br />
        WHERE FUN AND INFORMATIVE GRAPHS
        <br />
        <br />
        <br />
        WILL EVENTUALLY LIVE!
        <br />
        <br />
        <br />
      </p>
    
    <!--Added in the submit and cancel buttons and functions from the n card.
    It doesn't seem to me that the submit button is working, but I don't know 
    how to test it appropriately. -->
    <div style="text-align: right; margin-top: 1em">
      <UsaButton class="primary-button" @click="submit()"> Export </UsaButton>
      <UsaButton class="secondary-button" @click="cancel()"> Cancel </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>

  </NuxtLayout>
</template>

<script setup lang="ts">
const path = ref([
  {
    href: "/",
    text: "Artifact Store",
  },
  {
    href: "/report-card",
    text: "Report",
  },
]);

// Rewrote the form so that every item is at the top level;
// not sure that is exactly what we want but I figured it is a starting point.
const form = ref({
  model_summary: "",
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
    mlte_evaluation: "",
    intended_use: "",
    risks: "",
    data: "",
    caveats: "",
    analysis: "",
});

// did not change this function
function cancel() {
  if (
    confirm(
      "Are you sure you want to leave this page? All changes will be lost.",
    )
  ) {
    location.href = "/";
  }
}

// did not change this function
function submit() {
  console.log(form.value);
  console.log(useRoute().query.namespace);
}

// TODO: figure out how to actually have this function do something!!
// right now it is just a copy of submit()
function exporting() {
  console.log(form.value);
  console.log(useRoute().query.namespace);
}

// rewrote this function to work for the new form, but am not really
// sure how it works so have not called it anywhere...
function descriptorUpload(event: Event, descriptorName: string) {
  const target = event.target as HTMLInputElement;
  const file = target.files![0];
  if (file !== null) {
    const reader = new FileReader();
    reader.onload = (inputFile) => {
      try {
        const document = JSON.parse((inputFile.target!.result as string) ?? "");
        form.value.model_summary = document.model_summary;
        document.goals.forEach(
            (goal: {
              id: string;
              goal: string;
              metric: string;
              baseline: string;
            }) => {
              addGoal();
              const lastGoalIndex = form.value.goals.length - 1;

              form.value.goals[lastGoalIndex].description = goal.goal;
              form.value.goals[lastGoalIndex].metrics[0].description =
                goal.metric;
              form.value.goals[lastGoalIndex].metrics[0].baseline =
                goal.baseline;
            },
          );
          form.value.mlte_evaluation = document.mlte_evaluation;
          form.value.intended_use = document.intended_use;
          form.value.risks = document.risks;
          form.value.data = document.data;
          form.value.caveats = document.caveats;
          form.value.analysis = document.analysis;

          let outputString = "";
          // if (form.value.model.production.environment.output !== "") {
          //   outputString += "\n\n";
          // }
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
          // form.value.model.production.environment.output += outputString;
      } catch (err) {
        console.error("Invalid JSON or error in parsing file.");
      }
    };
    reader.readAsText(file);
  }
}

function addGoal() {
  form.value.goals.push({
    description: "",
    metrics: [{ description: "", baseline: "" }],
  });
}

function deleteGoal(goalIndex: number) {
  if (confirm("Are you sure you want to delete this goal?")) {
    form.value.goals.splice(goalIndex, 1);
  }
}

function addMetric(goalIndex: number) {
  form.value.goals[goalIndex].metrics.push({
    description: "",
    baseline: "",
  });
}

function deleteMetric(goalIndex: number, metricIndex: number) {
  if (confirm("Are you sure you want to delete this metric?")) {
    form.value.goals[goalIndex].metrics.splice(metricIndex, 1);
  }
}

</script> 