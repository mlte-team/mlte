<template>
  <div>
    <h3 class="no-margin-sub-header" style="display: inline-block">
      <slot />
      <ExampleButton v-if="props.renderExample" @click="visible = true" />
    </h3>
    <TemplatesModalWrapper
      :visible="visible"
      @toggle-visible="(value) => (visible = value)"
    >
      <template #heading> Example: </template>
      <slot name="example" />
    </TemplatesModalWrapper>
    <p v-if="props.renderInfo">
      <slot name="info" />
    </p>
  </div>
</template>

<script setup>
const visible = ref(false);

const props = defineProps({
  renderExample: {
    type: Boolean,
    required: false,
    default: true,
  },
  renderInfo: {
    type: Boolean,
    required: false,
    default: true,
  },
});
</script>
