<template>
    <div>
      <br/>
      <p>Inference latency is the time taken for a machine learning model to process an input and produce an output. For a flower classification model on a handheld device, low latency is crucial for providing immediate feedback to users and conserving battery life by reducing the computational load.</p>
      <br/>
      <!-- 1st stage-->
      <h2><b> Hardware Use </b></h2>
      <label><b>Prediction Timing (or Type?)</b></label>
      <USelect
        placeholder="Select an option..."
        :options="['Real time', 'Offline', 'Batch Processing']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="deploymentInfrastructure"
      />
      <p>Info tip: with batch prediction, you don’t need to worry about the inference latency. With online prediction, however, inference latency is crucial.</p>
      <br/>

      <label><b> Inference Optimization Techniques</b></label>
      <USelect
        placeholder="Select an option..."
        :options="['Model Quantization', 'Pruning', 'Specialized Hardware', 'Other']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="strategies"
      />
      <p>Info Tip: Techniques such as model quantization and pruning can significantly reduce inference latency. Specialized hardware can also improve performance.</p>
      <br/>

      <label><b> Trade-offs to Consider:</b></label>
      <ul>
        <li><b> - Latency vs. Throughput: </b>Optimizing for latency can sometimes reduce throughput, meaning the system can process fewer requests per second. How will you balance the need for low latency with the required throughput for your application?</li>
        <li><b> - Latency vs. Model Size:</b> Larger models generally require more processing time, which can increase latency. How will you manage the tradeoff between model complexity and the need for quick response times?</li>
    </ul>

    <br/>

     <!-- 2nd stage-->
     <h2><b> 2) Deployment</b></h2>

      <label><b>Deployment Infrastructure</b></label>
      <USelect
        placeholder="Select an option..."
        :options="['Cloud', 'On-premise', 'Edge']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="infrastructureDetails"
      />
      <p>Info Tip: recommendation here for each option </p>
      <br/>
  
     <!-- 3rd stage-->
     <h2><b> 3) Monitoring</b></h2>
      <label><b>Does your model need monitoring after deployment?</b></label>
      <USelect
        placeholder="Select an option..."
        :options="['Yes', 'No', 'to be defined']"
        icon="i-heroicons-magnifying-glass-20-solid"
        v-model="monitoringNeed"
      />
      <p>Info Tip: Frequent retraining can impact both training and inference latency. Plan retraining schedules carefully to balance performance and resource usage.</p>
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
  