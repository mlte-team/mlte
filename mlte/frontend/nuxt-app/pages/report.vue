<template>
  <NuxtLayout name="base-layout">
    <UsaBreadcrumb :items="path" />

    <h1 class="section-header">MLTE REPORT</h1>

    <h3>Model Summary</h3>
    <UsaTextarea>
      <template #label> Summary of the model being evaluated. </template>
      <!-- Note that when I type in this text box, 
            it clicks out of the area every time I type a letter.
          The same thing happens in the negotiation card
          in a few of the text boxes, so we need to fix that. -->
    </UsaTextarea>

    <!-- Kept the goals section consistent with the negotiation card.
    Probably need to rewrite once we figure out how we want to pull 
    sections from the negotiation card.-->
    <h3>Goals of the System</h3>
    <p>Goals or objectives that the model helps to satisfy.</p>
    <div v-for="(goal, goalIndex) in form.goals" :key="goal.description">
      <h3>Goal {{ goalIndex + 1 }}</h3>

      <UsaTextInput v-model="goal.description">
        <template #label> Goal Description </template>
      </UsaTextInput>
    </div>
    <AddButton class="margin-button" @click="addGoal()"> Add goal </AddButton>

    <h3>MLTE Evaluation</h3>
    <p>
      THIS IS A PLACEHOLDER
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
      <template #label> Description of model and system risks. </template>
    </UsaTextarea>

    <h3>Data</h3>
    <UsaTextarea>
      <template #label> Description of data used to train the model. </template>
    </UsaTextarea>

    <h3>Caveats and Recommendations</h3>
    <UsaTextarea>
      <template #label>
        Description of any caveats and recommendations for the system or model.
      </template>
    </UsaTextarea>

    <h3>Quantitative Analysis</h3>
    <p>
      THIS IS A PLACEHOLDER
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

    <!--Added in the submit and cancel buttons and functions from the negotiation card.
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
    href: "/here",
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

// Cancel editing of a report.
function cancel() {
  if (
    confirm(
      "Are you sure you want to leave this page? All changes will be lost.",
    )
  ) {
    location.href = "/";
  }
}

// TODO(Kyle): populate.
function submit() {
  console.log(form.value);
  console.log(useRoute().query.namespace);
}

function addGoal() {
  form.value.goals.push({
    description: "",
    metrics: [{ description: "", baseline: "" }],
  });
}
</script>
