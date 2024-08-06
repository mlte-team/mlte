<template>
    <div>
      <br/>
      <p>Training latency is the time it takes to train a machine learning model on a dataset. For a flower classification model on a handheld device, low training latency is crucial for quickly updating the model with new data, ensuring it remains accurate and effective without causing extended delays in development or updates.</p>
      <br/>
      <!-- 1st stage-->
      <h2><b> </b></h2>
      <label><b> Potential frameworks</b></label>

      <USelect
        placeholder="Select an option..."
        :options="['TensorFlow', 'pyTorch', 'Scikit-learn', 'Keras']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="deploymentInfrastructure"
      />
      <p>Info tip:  provide feedback about the </p>
      <br/>

      <label><b>Frequency of retraining </b></label>
      <USelect
        placeholder="Select an option..."
        :options="['Never', 'TBD']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="strategies"
      />
      <p>Info Tip: retraining </p>
      <br/>

      <label><b> Are you considering energy usage and carbon footprint in your model? 
    </b></label>
      <USelect
        placeholder="Select an option..."
        :options="['Yes', 'No']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="strategies"
      />
      <p>Info Tip: retraining </p>
      <br/>

      <label><b> Trade-offs to Consider:</b></label>
      <ul>
        <li><b> - Model Accuracy vs. Training Speed:</b></li>
        <li><b> - Feature Engineering vs. Training Speed</b> </li>
    </ul>

    <br/>

    </div>
  </template>
  
  <script lang="ts">
  import { ref } from 'vue';
  
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
  