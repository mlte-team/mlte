<template>
  <div>
    <div v-if="!newUserFlag">
      <div class="flex-container">
        <h1 class="section-header">{{ modelValue.username }}</h1>
        <div
          class="centered-container"
          style="vertical-align: bottom; padding-left: 33ch"
        >
          <div v-if="!resetPasswordFlag">
            <UsaButton class="secondary-button" @click="enablePasswordReset">
              Reset Password
            </UsaButton>
          </div>
          <div v-if="resetPasswordFlag">
            <UsaButton class="secondary-button" @click="disablePasswordReset">
              Cancel Reset
            </UsaButton>
          </div>
        </div>
      </div>
      <div v-if="resetPasswordFlag">
        <UsaTextInput
          v-model="modelValue.password"
          :error="formErrors.password"
          type="password"
        >
          <template #label> New Password </template>
          <template #error-message> Password is required </template>
        </UsaTextInput>
        <UsaTextInput
          v-model="confirmPassword"
          :error="formErrors.confirmPassword"
          type="password"
        >
          <template #label> Confirm New Password </template>
          <template #error-message> Passwords to not match </template>
        </UsaTextInput>
      </div>
    </div>
    <div v-if="newUserFlag">
      <UsaTextInput v-model="modelValue.username" :error="formErrors.username">
        <template #label> Username </template>
        <template #error-message> Username is required </template>
      </UsaTextInput>

      <UsaTextInput
        v-model="modelValue.password"
        :error="formErrors.password"
        type="password"
      >
        <template #label> Password </template>
        <template #error-message> Password is required </template>
      </UsaTextInput>
    </div>

    <UsaTextInput v-model="modelValue.email">
      <template #label> Email </template>
    </UsaTextInput>

    <UsaTextInput v-model="modelValue.full_name">
      <template #label> Full Name </template>
    </UsaTextInput>

    <UsaCheckbox v-model="modelValue.disabled" label="Disabled" />

    <UsaSelect
      v-model="modelValue.role"
      :options="roleOptions"
      :error="formErrors.role"
      @change="formErrors.role = false"
    >
      <template #label> Role </template>
      <template #error-message> A role must be selected </template>
    </UsaSelect>

    <label class="usa-label">Groups</label>
    <div v-for="groupOption in groupOptions" :key="groupOption.name">
      <UsaCheckbox
        v-model="groupOption.selected"
        :label="groupOption.name"
        @update:modelValue="groupChange(groupOption.selected, groupOption)"
      />
    </div>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="$emit('cancel')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit"> Save </UsaButton>
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
  newUserFlag: {
    type: Boolean,
    required: true,
    default: false,
  },
});

const resetPasswordFlag = ref(false);
const confirmPassword = ref("");
const roleOptions = ref([
  { value: "admin", text: "admin" },
  { value: "regular", text: "regular" },
]);
const formErrors = ref({
  username: false,
  role: false,
  password: false,
  confirmPassword: false,
});
const groupOptions = ref<
  { name: string; permissions: Array<object>; selected: boolean }[]
>([]);
const { data: groupList } = await useFetch<string[]>(
  config.public.apiPath + "/groups/details",
  {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token.value,
    },
  },
);
if (groupList.value) {
  groupList.value.forEach((group: object) => {
    groupOptions.value.push({
      name: group.name,
      permissions: group.permissions,
      selected: false,
    });
  });
}

groupOptions.value.forEach((groupOption) => {
  if (props.modelValue.groups.find((x) => x.name === groupOption.name)) {
    groupOption.selected = true;
  }
});

function enablePasswordReset() {
  resetPasswordFlag.value = true;
  props.modelValue.password = "";
}

function disablePasswordReset() {
  resetPasswordFlag.value = false;
  delete props.modelValue.password;
}

function groupChange(selected: boolean, groupOption: object) {
  if (selected) {
    props.modelValue.groups.push({
      name: groupOption.name,
      permissions: groupOption.permissions,
    });
  } else {
    const objForRemoval = props.modelValue.groups.find(
      (x) => x.name === groupOption.name,
    );
    const index = props.modelValue.groups.indexOf(objForRemoval);
    props.modelValue.groups.splice(index, 1);
  }
}

function submit() {
  resetFormErrors();
  let submitError = false;

  if (props.newUserFlag) {
    if (props.modelValue.username.trim() === "") {
      formErrors.value.username = true;
      submitError = true;
    }

    if (props.modelValue.password.trim() === "") {
      formErrors.value.password = true;
      submitError = true;
    }
  }

  if (resetPasswordFlag.value) {
    if (props.modelValue.password.trim() === "") {
      formErrors.value.password = true;
      submitError = true;
    }
    if (props.modelValue.password !== confirmPassword.value) {
      formErrors.value.confirmPassword = true;
      submitError = true;
    }
  }

  if (props.modelValue.role.trim() === "") {
    formErrors.value.role = true;
    submitError = true;
  }

  if (!submitError) {
    emit("submit", props.modelValue);
  }
}

function resetFormErrors() {
  formErrors.value.username = false;
  formErrors.value.role = false;
  formErrors.value.password = false;
  formErrors.value.confirmPassword = false;
}
</script>
