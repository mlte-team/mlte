<template>
  <div>
    <UsaSelect
      :model-value="modelValue"
      :disabled="props.disabled"
      :options="options"
      @update:model-value="emit('update:modelValue', $event)"
    >
      <template #label>
        <slot name="label" />
        <TemplatesTooltipInfo>
          <slot name="tooltip" />
        </TemplatesTooltipInfo>
      </template>
    </UsaSelect>

    <div v-if="modelValue === 'Other'">
      <div class="inline-input-left" style="width: 30rem">
        <UsaTextInput v-model="newOption">
          <template #label> New <slot name="label" /> </template>
        </UsaTextInput>
      </div>

      <div class="inline-button">
        <UsaButton
          class="secondary-button"
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
  options: {
    type: Array<SelectOption>,
    required: true,
  },
});

const newOption = ref("");
</script>
