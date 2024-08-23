<template>
  <div class="input-group" style="margin-top: 1em">
    <SubHeader>
      Production Compute Resources
      <template #example>
        Example: GPUs = 2, CPUs = 2, Memory = 256 MB, Storage = 512 MB
      </template>
      <template #info>
        Describe the amount and type of compute resources needed for
        inference.
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