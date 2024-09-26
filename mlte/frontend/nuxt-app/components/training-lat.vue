<template>
  <div>
    <br />
    <p>Training latency is the time it takes to train a machine learning model on a dataset. For a flower classification model on a handheld device, low training latency is crucial for quickly updating the model with new data, ensuring it remains accurate and effective without causing extended delays in development or updates.</p>
    <br />
    <h2><b> </b></h2>

    <label><b>Deployment Infrastructure</b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Cloud', 'On-premise', 'Edge']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="infrastructureDetails"
    >
      <template v-slot:info-icon>
        <i-heroicons-information-circle-20-solid />
        <p>Info Tip: This field represents the environment where the model will be deployed. Choose the most suitable option based on your project's requirements.</p>
      </template>
    </USelect>
    <br />

    <label><b>Frequency of retraining </b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Never', 'To be defined']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="strategies"
    >
      <template v-slot:info-icon>
        <i-heroicons-information-circle-20-solid />
        <p>Info Tip: Indicate how often the model will need to be retrained with new data to maintain its accuracy and relevance.</p>
      </template>
    </USelect>
    <br />

    <label><b> Are you considering energy usage and carbon footprint in your model?</b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Yes', 'No']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="strategies"
    >
      <template v-slot:info-icon>
        <i-heroicons-information-circle-20-solid />
        <p>Info Tip: Consider the environmental impact of your model's training and deployment processes, especially in terms of energy consumption and carbon emissions.</p>
      </template>
    </USelect>
    <br />

    <label><b> Trade-offs to Consider:</b></label>
    <ul>
      <li><b> - Model Accuracy vs. Training Speed:</b></li>
      <li><b> - Feature Engineering vs. Training Speed</b> </li>
    </ul>

    <br />
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';

// data from the negotiation card 
export default {
  name: 'InferenceLatencyForm',
  props: {
    MLTask: {
      type: String,
      required: true,
    },
    usageContext: {
      type: String,
      required: true,
    },
  },
  setup() {
    // reactive vars
    const deploymentInfrastructure = ref<string | null>(null);
    const infrastructureDetails = ref<string | null>(null);

    return {
      deploymentInfrastructure,
      infrastructureDetails,
    };
  },
};
</script>

<style scoped>
</style>