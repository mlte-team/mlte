<template>
  <div>
    <br />
    <!-- API call -->
    <div class="chatgptcall">
      <p>
        Explainability refers to the ability to describe the decisions of a machine learning model in a way that is understandable to the end users.
        <span class="AIgeneratedtext">{{ response }} </span>
      </p>
    </div>
    <br />

<div>
    <!-- Deployment Option -->
    <label><b>List the project stakeholders</b></label>
    <div class="info-container">
      <span class="info-icon">i</span>
      <div class="tooltip">edit this...</div>
    </div>
    <UInput size="sm" />
    <br />

    <!-- Deployment Infrastructure -->
    <label><b>Purpose of the explanations</b></label>
    <div class="info-container">
      <span class="info-icon">i</span>
      <div class="tooltip">Select where your model will be deployed</div>
    </div>
    <UInput size="sm" />
    <br />

    <!-- Inference Latency Metrics -->
    <label><b>Indicate the goal of the explanations in your system</b></label>
    <UInput size="sm" />
    <br />

    <!-- Dynamic Sentence -->
    <p class="input-group" style="padding-top: 10px; padding-bottom: 10px">
  <b>Scenario for Explainability:</b> Model needs explainations for {{ deploymentInfrastructure }}. The stakeholders are motivated to understand the model due to {{ averageLatency }}.
</p>


  </div>





    <!-- <ul>
      <li>
        <b> - Latency vs. Throughput:</b> Optimizing for latency can sometimes reduce throughput, meaning the system can process fewer requests per second. How will you balance the need for low latency with the required throughput for your application?
      </li>
      <li>
        <b> - Latency vs. Model Size:</b> Larger models generally require more processing time, which can increase latency. How will you manage the tradeoff between model complexity and the need for quick response times?
      </li>
    </ul> -->
  </div>

<!-- -->

<p> </p>

</template>

<script lang="ts">
import { ref, onMounted, computed } from 'vue';
import { openai } from '~/composables/openai';

export default {
  name: 'InferenceLatencyForm',
  props: {
    MLTask: {
      required: true,
    },
    usageContext: {
      required: true,
    },
  },
  setup(props) {
    const response = ref('');
    const deploymentInfrastructure = ref<string | null>(null);
    const infrastructureDetails = ref<string | null>(null);
    const averageLatency = ref<string | null>(null);
    const mostLatency = ref<string | null>(null);
    const latencySeconds = ref<string | null>(null);

    //  first word of deploymentInfrastructure and detailsa
    const firstWordOfDeploymentInfrastructure = computed(() => {
      if (deploymentInfrastructure.value) {
        return deploymentInfrastructure.value.split(' ')[0]; 
      }
      return '';
    });

    const firstWordOfinfrastructureDetails = computed(() => {
      if (infrastructureDetails.value) {
        return infrastructureDetails.value.split(' ')[0]; 
      }
      return '';
    });

    const chat_role = 'You are a specialized data scientist with knowledge in both software engineering and data science.';

    const getChatResponse = async () => {
      const { chat } = openai();
      try {
        const messages = [
          {
            role: 'system',
            content: chat_role,
          },
          {
            role: 'user',
            content: `Write one sentence to explain the potential consequences of not considering explainability needs in the context of ${props.MLTask} and ${props.usageContext}. Use simple language that data scientists would understand`,
          },
        ];

        const chatResponse = await chat(messages, 'gpt-3.5-turbo');
        const splitResponse = chatResponse.split('\n\n');
        response.value = splitResponse[0];
      } catch (error) {
        console.error('Error fetching chat response:', error);
      }
    };

    onMounted(() => {
      getChatResponse();
    });

    return {
      response,
      deploymentInfrastructure,
      infrastructureDetails,
      averageLatency,
      mostLatency,
      latencySeconds,
      firstWordOfDeploymentInfrastructure, 
      firstWordOfinfrastructureDetails,
    };
  },
};
</script>


<style scoped>
.AIgeneratedtext{
  background-color: #efe8c7;
}

.info-icon {
  display: inline-block;
  width: 20px;
  height: 20px;
  background-color: black;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-weight: bold;
  font-family: Arial, cursive;
  font-size: 10px;
  cursor: pointer;
  margin-left: 5px;
  position: relative;
}

.tooltip {
  display: none;
  position: absolute;
  background-color: rgb(0, 0, 0);
  color: rgb(255, 255, 255);
  border: 1px solid #ccc;
  padding: 10px;
  font-size: 12px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 200px;
  top: 25px; 
  left: 0;
  z-index: 10;
}

.info-container:hover .tooltip {
  display: block;
}

.info-container {
  position: relative;
  display: inline-block;
}
</style>
