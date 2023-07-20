<template>
  <div style="margin-bottom: 1em">
    <UsaButton variant="unstyled" @click="$emit('select')">
      <slot />
    </UsaButton>
    <UsaButton variant="unstyled" style="float: right" @click="$emit('delete')">
      <img src="~/assets/uswds/img/usa-icons/delete.svg" class="usa-icon" />
    </UsaButton>
  </div>
</template>
