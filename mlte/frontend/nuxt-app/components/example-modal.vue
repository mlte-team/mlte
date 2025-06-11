<template>
  <UsaModal
    :visible="props.visible"
    :force-action="false"
    size="lg"
    @update:visible="$emit('toggleVisible', false)"
  >
    <template #close-button>
      <button
        type="button"
        class="usa-button usa-modal__close"
        aria-label="Close this window"
        @click="emit('toggleVisible', false)"
      >
        <img
          src="~/assets/uswds/img/usa-icons/close.svg"
          class="inline-icon usa-icon"
        />
      </button>
    </template>
    <template #heading> Example: </template>
    <slot />
    <template #footer>
      <slot name="footer" />
    </template>
  </UsaModal>
</template>

<script setup>
const emit = defineEmits(["toggleVisible"]);
const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
});
</script>
