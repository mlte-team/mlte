<template>
  <UsaCheckbox
    :model-value="props.selected"
    @update:modelValue="$emit('update')"
  >
    <slot />
    <UsaButton
      variant="unstyled"
      style="float: right; margin-right: 10px"
      @click="$emit('delete')"
    >
      <img src="~/assets/uswds/img/usa-icons/delete.svg" class="usa-icon" />
    </UsaButton>
  </UsaCheckbox>
</template>

<script setup>
const props = defineProps({
  selected: {
    type: Boolean,
    required: true,
  },
});
</script>
