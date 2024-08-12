<template>
  <div>
    <!-- <input v-model="userMessage" placeholder="Ask a question..." />
    <button @click="getChatResponse">Send</button> -->
    <p>{{ response }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { openai } from '~/composables/openai'

//const userMessage = ref('')
const response = ref('')

const chatrole = "You are a specialized data scientist with knowledge in both software engineering and data science. You are aware of how the model of a data scientist is going to be used. Your language is targeted at data scientists. Your goal is to translate terminology used by software engineers and product owners to communicate product aspects to data scientists. Often, data scientists disregard important product requirements and tend to focus on model accuracy. You communicate product terminology clearly and use friendly but professional language."

const getChatResponse = async () => {
  const { chat } = openai()
  try {
    const messages = [
      { role: 'user', content: "what's latency?" },
      { role: 'system', content: chatrole }  
    ];
    response.value = await chat(messages, 'gpt-3.5-turbo');
  } catch (error) {
    console.error('Error fetching chat response:', error)
  }
}
onMounted(() => {
  getChatResponse();
});
</script>
