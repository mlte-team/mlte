<script setup>
import { ref, onMounted } from 'vue'
const { chatCompletion } = useChatgpt()

const chatTree = ref([
  {
    role: 'system',
    content: 'You are a specialized data scientist with knowledge in both software engineering and data science. You are aware of how the model of a data scientist is going to be used. Your language is targeted at data scientists. Your goal is to translate terminology used by software engineers and product owners to communicate product aspects to data scientists. Often, data scientists disregard important product requirements and tend to focus on model accuracy. You communicate product terminology clearly and use friendly but professional language.'
  },
  {
    role: 'user',
    content: 'What are the best practices for integrating machine learning models into software engineering workflows?'
  }
])

const inputData = ref('')

async function sendMessage() {
  try {
    const response = await chatCompletion(chatTree.value)
    
    const responseMessage = {
      role: response[0].message.role,
      content: response[0].message.content
    }
    
    chatTree.value.push(responseMessage)
  } catch(error) {
    alert(`Join the waiting list if you want to use GPT-4 models: ${error}`)
  }
}

// Automatically send the message when the component is mounted
onMounted(() => {
  sendMessage()
})
</script>


<template>
  <div>
    <div>
      <div
        v-for="chat in chatTree.filter(chat => chat.role === 'assistant')"
        :key="chat.content"
      >
        <div>{{ chat.content }}</div>
      </div>
    </div>
  </div>
</template>
