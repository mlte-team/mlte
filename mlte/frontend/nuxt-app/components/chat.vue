<template>
    <NuxtLayout name="base-layout">
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
    </NuxtLayout>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useChatgpt } from 'nuxt-chatgpt';
  
  interface ChatMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
  }
  
  const { chatCompletion } = useChatgpt();
  
  const chatTree = ref<ChatMessage[]>([
    {
      role: 'system',
      content: 'You are a specialized data scientist with knowledge in both software engineering and data science. You are aware of how the model of a data scientist is going to be used. Your language is targeted at data scientists. Your goal is to translate terminology used by software engineers and product owners to communicate product aspects to data scientists. Often, data scientists disregard important product requirements and tend to focus on model accuracy. You communicate product terminology clearly and use friendly but professional language.'
    },
    {
      role: 'user',
      content: 'What are the best practices for integrating machine learning models into software engineering workflows?'
    }
  ]);
  
  async function sendMessage(): Promise<void> {
    try {
      const response = await chatCompletion(chatTree.value);
      
      const responseMessage: ChatMessage = {
        role: response[0].message.role,
        content: response[0].message.content
      };
      
      chatTree.value.push(responseMessage);
    } catch(error) {
      console.error('Error in sendMessage:', error);
      alert(`Join the waiting list if you want to use GPT-4 models: ${error}`);
    }
  }
  
  // Automatically send the message when the component is mounted
  onMounted((): void => {
    sendMessage();
  });
  </script>
  