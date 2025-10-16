<template>
  <div style="margin-bottom: 1em">
    <h2 class="section-header" style="display: inline">
      <slot name="title" />
    </h2>
    <UsaButton
      v-if="!modelValue"
      class="secondary-button"
      @click="$emit('change', true)"
    >
      Show
    </UsaButton>
    <UsaButton v-else class="secondary-button" @click="$emit('change', false)">
      Hide
    </UsaButton>
  </div>
</template>

<script setup lang="ts">
const emits = defineEmits(["change"]);

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});
</script>
