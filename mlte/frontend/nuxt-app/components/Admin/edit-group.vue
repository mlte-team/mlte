<template>
  <div>
    <div v-if="!newGroupFlag">
      <h1 class="section-header">{{ modelValue.name }}</h1>
    </div>
    <div v-if="newGroupFlag">
      <UsaTextInput v-model="modelValue.name" :error="formErrors.name">
        <template #label> Group Name </template>
        <template #error-message> Group name is required </template>
      </UsaTextInput>
    </div>

    <label class="usa-label">Permissions</label>
    <div v-for="(permissionOption, index) in permissionOptions" :key="index">
      <UsaCheckbox
        v-model="permissionOption.selected"
        @update:modelValue="
          permissionChange(permissionOption.selected, permission)
        "
      >
        <template #default>
          <span v-if="permissionOption.resource_id === null">
            {{ permissionOption.resource_type }} - (All) -
            {{ permissionOption.method }}
          </span>
          <span v-else>
            {{ permissionOption.resource_type }} -
            {{ permissionOption.resource_id }} -
            {{ permissionOption.method }}
          </span>
        </template>
      </UsaCheckbox>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");

const emit = defineEmits(["cancel", "submit", "updateUserGroups"]);
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: {},
  },
  newGroupFlag: {
    type: Boolean,
    required: true,
    default: false,
  },
});

const permissionOptions = ref<
  {
    resource_type: string;
    resource_id: string;
    method: string;
    selected: boolean;
  }[]
>([
  {
    resource_id: "blah",
    resource_type: "model",
    method: "get",
    selected: false,
  },
  {
    resource_id: "blah",
    resource_type: "model",
    method: "post",
    selected: false,
  },
  {
    resource_id: "blah",
    resource_type: "model",
    method: "delete",
    selected: false,
  },
]);
// const { data: permissionList } = await useFetch<string[]>(
//   config.public.apiPath + "/TBD",
//   {
//     method: "GET",
//     headers: {
//       Authorization: "Bearer " + token.value,
//     },
//   },
// );
// if (permissionList.value) {
//   permissionList.value.forEach((permission: object) => {
//     permissionOptions.value.push({ resource_id: permission.resource_id, resource_type: permission.resource_type, method: permission.method, selected: false });
//   });
// }

// permissionOptions.value.forEach((permissionOption) => {
//   if (props.modelValue.permissions.find((x) => x === permissionOption)) {
//     permissionOption.selected = true;
//   }
// })

function permissionChange(selected: boolean, permissionOption: object) {
  if (selected) {
    props.modelValue.permissions.push({
      resource_id: permissionOption.resource_id,
      resource_type: permissionOption.resource_type,
      method: permissionOption.method,
    });
  } else {
    const objForRemoval = props.modelValue.permissions.find(
      (x) => x.name === permissionOption.name,
    );
    const index = props.modelValue.permissions.indexOf(objForRemoval);
    props.modelValue.permissions.splice(index, 1);
  }
}
</script>
