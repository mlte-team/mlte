<template>
  <div>
    <h3 class="no-margin-sub-header" style="display: inline-block">
      <slot />
      <UsaButton
        v-if="props.renderExample"
        class="secondary-button"
        @click="exampleVisible = true"
      >
        Example
      </UsaButton>
      <NuxtLink
        v-if="props.renderModel"
        target="_blank"
        :to="{
          path: '/etc/quality-model',
        }"
      >
        <UsaButton class="secondary-button"> View Quality Model </UsaButton>
      </NuxtLink>
    </h3>
    <TemplatesModalWrapper
      :visible="exampleVisible"
      @toggle-visible="(value) => (exampleVisible = value)"
    >
      <template #heading>Example:</template>
      <slot name="example" />
    </TemplatesModalWrapper>
    <p v-if="props.renderInfo">
      <slot name="info" />
    </p>
  </div>
</template>

<script setup>
const exampleVisible = ref(false);

const props = defineProps({
  renderExample: {
    type: Boolean,
    required: false,
    default: true,
  },
  renderModel: {
    type: Boolean,
    required: false,
    default: false,
  },
  renderInfo: {
    type: Boolean,
    required: false,
    default: true,
  },
});
</script>
