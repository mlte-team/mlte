<template>
  <span v-if="props.measurement">
    <b>Measurement</b>
    <ul>
      <li>
        <b>Measurement Class: </b>{{ props.measurement.measurement_class }}
      </li>
      <li><b>Output Class: </b>{{ props.measurement.output_class }}</li>
      <li v-if="Object.keys(props.measurement.additional_data).length !== 0">
        <b>Additional Data</b>
        <ul>
          <li
            v-for="(value, key) in props.measurement.additional_data"
            :key="key"
          >
            {{ key }}: {{ value }}
          </li>
        </ul>
      </li>
    </ul>
  </span>
  <span v-else> <b>Measurement:</b> null </span>
</template>

<script setup lang="ts">
interface Props {
  measurement?: MeasurementMetadata | null;
}

const props = withDefaults(defineProps<Props>(), {
  measurement: null,
});
</script>
