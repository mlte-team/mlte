<template>
  <div style="margin-bottom: 1em;">
    <UsaButton variant="unstyled" @click="this.$emit('select')">
      <slot/>
    </UsaButton>
    <UsaButton variant="unstyled" style="float: right;" @click="this.$emit('delete')">
      <img src="~/assets/uswds/img/usa-icons/delete.svg" class="usa-icon"/>
    </UsaButton>
  </div>
</template>