<template>
  <TemplatesModalWrapper
    :visible="visible"
    @toggle-visible="emit('toggleVisible')"
  >
    <template #heading> Test Suite Template</template>
    <label class="usa-label">
      <CopyIcon @click="copyToClipboard(props.modelValue)" />
    </label>
    <Codemirror :model-value="props.modelValue" :extensions="extensions" />
  </TemplatesModalWrapper>
</template>

<script setup lang="ts">
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
const extensions = [python()];
const { copyToClipboard } = useCopyToClipboard();

const emit = defineEmits(["toggleVisible"]);
const props = defineProps({
  modelValue: {
    type: String,
    required: true,
  },
  visible: {
    type: Boolean,
    required: true,
  },
});
</script>
