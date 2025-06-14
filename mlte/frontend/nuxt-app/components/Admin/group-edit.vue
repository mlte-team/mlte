<template>
  <div>
    <div v-if="!newGroupFlag">
      <h2 class="section-header">{{ modelValue.name }}</h2>
    </div>
    <div v-if="newGroupFlag">
      <UsaTextInput v-model="modelValue.name" :error="formErrors.name">
        <template #label> Group Name </template>
        <template #error-message> Group name is required </template>
      </UsaTextInput>
    </div>

    <label class="usa-label">Permissions</label>
    <div class="multi-line-checkbox-div">
      <span
        v-for="(permissionOption, index) in permissionOptions"
        :key="index"
        class="multiple-per-line-checkbox"
      >
        <UsaCheckbox
          v-model="permissionOption.selected"
          @update:model-value="
            permissionChange(permissionOption.selected, permissionOption)
          "
        >
          <span v-if="permissionOption.resource_id === null">
            {{ permissionOption.resource_type }} - (All) -
            {{ permissionOption.method }}
          </span>
          <span v-else>
            {{ permissionOption.resource_type }} -
            {{ permissionOption.resource_id }} -
            {{ permissionOption.method }}
          </span>
        </UsaCheckbox>
      </span>
    </div>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="emit('cancel')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit"> Save </UsaButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from "vue";

const config = useRuntimeConfig();
const token = useCookie("token");

const emit = defineEmits(["cancel", "submit"]);
const props = defineProps({
  modelValue: {
    type: Object as PropType<Group>,
    required: true,
  },
  newGroupFlag: {
    type: Boolean,
    required: true,
    default: false,
  },
});

const formErrors = ref<Dictionary<boolean>>({
  name: false,
});
const permissionOptions = ref<Array<PermissionCheckboxOption>>([]);
const { data: permissionList } = await useFetch<Array<Permission>>(
  config.public.apiPath + "/groups/permissions/details",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (permissionList.value) {
  permissionList.value.forEach((permission: Permission) => {
    permissionOptions.value.push(
      new PermissionCheckboxOption(
        permission.resource_type,
        permission.resource_id,
        permission.method,
        false,
      ),
    );
  });
}

permissionOptions.value.forEach((permissionOption) => {
  if (
    props.modelValue.permissions.find(
      (x: Permission) =>
        x.resource_type === permissionOption.resource_type &&
        x.resource_id === permissionOption.resource_id &&
        x.method === permissionOption.method,
    )
  ) {
    permissionOption.selected = true;
  }
});

function permissionChange(selected: boolean, permissionOption: Permission) {
  if (selected) {
    props.modelValue.permissions.push(
      new Permission(
        permissionOption.resource_type,
        permissionOption.resource_id,
        permissionOption.method,
      ),
    );
  } else {
    const objForRemoval = props.modelValue.permissions.find(
      (x: Permission) =>
        x.resource_type === permissionOption.resource_type &&
        x.resource_id === permissionOption.resource_id &&
        x.method === permissionOption.method,
    );
    // TODO: Add error handling
    if (objForRemoval) {
      const index = props.modelValue.permissions.indexOf(objForRemoval);
      props.modelValue.permissions.splice(index, 1);
    }
  }
}

function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (props.newGroupFlag) {
    if (props.modelValue.name.trim() === "") {
      formErrors.value.name = true;
      inputError = true;
    }
  }

  if (inputError) {
    return;
  }
  emit("submit", props.modelValue);
}
</script>
