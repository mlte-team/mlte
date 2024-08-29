<template>
  <div>
    <br />
    <div class="chatgptcall">
      <p>{{ response }}</p>
    </div>
    <br />

    <!-- Form starts here -->

    <label><b>Prediction Timing</b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Real time', 'Offline', 'Batch Processing', 'Other', 'To be defined']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="deploymentInfrastructure"
    />
    <p>Info tip: {{ recommendationTips[deploymentInfrastructure] }}</p>
    <br />

    <label><b>Inference Optimization Techniques</b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Model Quantization', 'Pruning', 'Specialized Hardware', 'Other', 'To be defined']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="strategies"
    />
    <p>Info Tip: Techniques such as model quantization and pruning can significantly reduce inference latency. Specialized hardware can also improve performance.</p>

    <br />

    <!-- 2nd stage-->

    <label><b>Deployment Infrastructure</b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Cloud', 'On-premise', 'Edge']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="infrastructureDetails"
    />
    <p>Info Tip: recommendation here for each option </p>
    <br />

    <!-- 3rd stage-->
    <label><b>Does your model need monitoring after deployment?</b></label>
    <USelect
      placeholder="Select an option..."
      :options="['Yes', 'No', 'to be defined']"
      icon="i-heroicons-magnifying-glass-20-solid"
      v-model="monitoringNeed"
    />
    <p>Info Tip: Frequent retraining can impact both training and inference latency. Plan retraining schedules carefully to balance performance and resource usage.</p>
    <br />

    <label><b>Trade-offs to Consider:</b></label>
    <ul>
      <li><b> - Latency vs. Throughput:</b> Optimizing for latency can sometimes reduce throughput, meaning the system can process fewer requests per second. How will you balance the need for low latency with the required throughput for your application?</li>
      <li><b> - Latency vs. Model Size:</b> Larger models generally require more processing time, which can increase latency. How will you manage the tradeoff between model complexity and the need for quick response times?</li>
    </ul>
    <br/>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import { openai } from '~/composables/openai';

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
  setup(props) {
    const response = ref('');
    const deploymentInfrastructure = ref<string | null>(null);
    const infrastructureDetails = ref<string | null>(null);
    const monitoringNeed = ref<string | null>(null);

    const recommendationTips = ref<Record<string, string>>({
      'Real time': '',
      'Offline': '',
      'Batch Processing': '',
      'Other': '',
      'To be defined': ''
    });

    const chat_role = "You are a specialized data scientist with knowledge in both software engineering and data science. You are aware of how the model of a data scientist is going to be used. Your language is targeted at data scientists. Your goal is to translate terminology used by software engineers and product owners to communicate product aspects to data scientists. Often, data scientists disregard important product requirements and tend to focus on model accuracy. You communicate product terminology clearly and use friendly but professional language."

    const getChatResponse = async () => {
      const { chat } = openai();
      try {
        const messages = [
          {
            role: 'system',
            content: chat_role
          },
          {
            role: 'user',
            content: `1. Write a two-sentence response that is easy to read and understand for data scientists describing what inference latency is and why it is important in the context of ${props.MLTask} and ${props.usageContext}.
              2. Also, provide recommendations for each option under "Prediction Timing" ('Real time', 'Offline', 'Batch Processing', 'Other', 'To be defined').`
          }
        ];

        const chatResponse = await chat(messages, 'gpt-3.5-turbo');

        const splitResponse = chatResponse.split("\n\n");

        response.value = splitResponse[0];

        const recommendations = {
          'Real time': splitResponse[1]?.match(/Real time: (.*)/)?.[1] || '',
          'Offline': splitResponse[1]?.match(/Offline: (.*)/)?.[1] || '',
          'Batch Processing': splitResponse[1]?.match(/Batch Processing: (.*)/)?.[1] || '',
          'Other': splitResponse[1]?.match(/Other: (.*)/)?.[1] || '',
          'To be defined': splitResponse[1]?.match(/To be defined: (.*)/)?.[1] || '',
        };

        recommendationTips.value = recommendations;

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
      recommendationTips,
      infrastructureDetails,
      monitoringNeed,
    };
  },
};
</script>

<style scoped>
</style>
