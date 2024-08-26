<template>
  <div class="input-group">
  <SubHeader>
    Development Compute Resources
    <template #example>
      GPUs = 2, CPUs = 1, Memory = 512 MB, Storage = 1 GB
    </template>
    <template #info>
      Describe the amount and type of compute resources needed for training.
    </template>
  </SubHeader>
  <div>
    <div class="inline-input-left">
      <UsaTextInput
        v-model="props.modelValue.gpu"
      >
        <template #label> Graphics Processing Units (GPUs) </template>
      </UsaTextInput>
    </div>

    <div class="inline-input-right">
      <UsaTextInput
        v-model="props.modelValue.cpu"
      >
        <template #label> Central Processing Units (CPUs) </template>
      </UsaTextInput>
    </div>
  </div>

  <div>
    <div class="inline-input-left">
      <UsaTextInput
        v-model="props.modelValue.memory"
      >
        <template #label> Memory </template>
      </UsaTextInput>
    </div>

    <div class="inline-input-right">
      <UsaTextInput
        v-model="props.modelValue.storage"
      >
        <template #label> Storage </template>
      </UsaTextInput>
    </div>
  </div>
</div>
</template>


<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: {
      gpu: 0,
      cpu: 0,
      memory: 0,
      storage: 0,
    },
  },
});
</script>
