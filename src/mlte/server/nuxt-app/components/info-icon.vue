<template>
  <UsaTooltip>
    <img src="~/assets/uswds/img/usa-icons/info.svg" class="inline-icon usa-icon"/>
    <template v-slot:label>
      <slot/>
    </template>
  </UsaTooltip>
</template>