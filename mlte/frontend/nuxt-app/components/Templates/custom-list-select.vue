<template>
  <div>
    <UsaSelect
      :model-value="modelValue"
      :disabled="props.disabled"
      :error="props.error && modelValue === 'Other'"
      :options="options"
      @update:model-value="emit('update:modelValue', $event)"
    >
      <template #label>
        <slot name="label" />
        <slot name="description" />
        <TemplatesTooltipInfo>
          <slot name="tooltip" />
        </TemplatesTooltipInfo>
      </template>
      <template #error-message>
        <slot name="error-message" />
      </template>
    </UsaSelect>
    <br />

    <div v-if="modelValue === 'Other'">
      <div class="inline-input-left" style="width: 30rem">
        <UsaTextInput v-model="newOption" :disabled="props.disabled">
          <template #label> <slot name="new-label" /> </template>
        </UsaTextInput>
      </div>

      <div class="inline-button">
        <UsaButton
          class="secondary-button"
          :disabled="props.disabled"
          @click="$emit('saveNewEntry', newOption)"
        >
          Save
        </UsaButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(["update:modelValue", "saveNewEntry"]);
const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  error: {
    type: Boolean,
    default: false,
  },
  options: {
    type: Array<SelectOption>,
    required: true,
  },
});

const newOption = ref("");
</script>
