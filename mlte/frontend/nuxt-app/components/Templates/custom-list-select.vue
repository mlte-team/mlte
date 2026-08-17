<template>
  <div class="inline-form-row">
    <div :class="modelValue === 'Other' ? 'grid-col-5' : 'grid-col-12'">
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
    </div>

    <template v-if="modelValue === 'Other'">
      <div class="grid-col-5">
        <UsaTextInput v-model="newOption" :disabled="props.disabled">
          <template #label>
            <slot name="new-label" />
          </template>
        </UsaTextInput>
      </div>

      <div class="grid-col-2">
        <UsaButton
          class="secondary-button"
          :disabled="props.disabled || !newOption.trim()"
          @click="handleSave"
        >
          Save
        </UsaButton>
      </div>
    </template>
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
    type: Array as PropType<SelectOption[]>,
    required: true,
  },
});

const newOption = ref("");

watch(
  () => props.modelValue,
  (val) => {
    if (val !== "Other") {
      newOption.value = "";
    }
  }
);

const handleSave = () => {
  if (!newOption.value.trim()) return;
  emit("saveNewEntry", newOption.value);
  newOption.value = "";
};
</script>
