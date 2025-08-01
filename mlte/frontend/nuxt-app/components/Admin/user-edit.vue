<template>
  <div>
    <div v-if="!newUserFlag">
      <h1 class="section-header" style="display: inline">
        {{ modelValue.username }}
      </h1>
      <UsaButton
        v-if="!changePasswordFlag"
        class="secondary-button sub-header-float-button"
        @click="enablePasswordReset"
      >
        Change Password
      </UsaButton>
      <UsaButton
        v-if="changePasswordFlag"
        class="secondary-button sub-header-float-button"
        @click="disablePasswordReset"
      >
        Cancel Change
      </UsaButton>

      <div v-if="changePasswordFlag">
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

    <div class="multi-line-checkbox-div">
      <label class="usa-label">Groups</label>
      <div v-if="newUserFlag">
        User will automatically be added to the <b>create-model</b> group upon
        submission.
      </div>
      <span
        v-for="groupOption in groupOptions"
        :key="groupOption.name"
        class="multiple-per-line-checkbox"
      >
        <UsaCheckbox
          v-model="groupOption.selected"
          @update:model-value="groupChange(groupOption.selected, groupOption)"
        >
          {{ groupOption.name }}
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

const emit = defineEmits(["cancel", "submit", "updateUserGroups"]);
const props = defineProps({
  modelValue: {
    type: Object as PropType<User>,
    required: true,
  },
  newUserFlag: {
    type: Boolean,
    required: true,
    default: false,
  },
});

const changePasswordFlag = ref(false);
const confirmPassword = ref("");
const roleOptions = ref([
  { value: "admin", text: "admin" },
  { value: "regular", text: "regular" },
]);
const formErrors = ref<Dictionary<boolean>>({
  username: false,
  role: false,
  password: false,
  confirmPassword: false,
});
const groupOptions = ref<Array<GroupCheckboxOption>>([]);
const groupList = ref<Array<Group>>([]);
groupList.value = await getGroupList();

if (groupList.value) {
  groupList.value.forEach((group: Group) => {
    groupOptions.value.push(
      new GroupCheckboxOption(group.name, group.permissions, false),
    );
  });
}

groupOptions.value.forEach((groupOption: GroupCheckboxOption) => {
  if (props.modelValue.groups.find((x: Group) => x.name === groupOption.name)) {
    groupOption.selected = true;
  }
});

if (props.newUserFlag) {
  props.modelValue.role = "regular";
}

// Enable the form fields to change password.
function enablePasswordReset() {
  changePasswordFlag.value = true;
  props.modelValue.password = "";
}

// Disable the form fields to change password.
function disablePasswordReset() {
  changePasswordFlag.value = false;
  delete props.modelValue.password;
}

/**
 * Handle a group change either adding the item to selections, or removing it.
 *
 * @param {boolean} selected Flag indicating if item was selected or deselected
 * @param {Group} groupOption Group that was selected or deselected
 */
function groupChange(selected: boolean, groupOption: Group) {
  if (selected) {
    props.modelValue.groups.push(
      new Group(groupOption.name, groupOption.permissions),
    );
  } else {
    const objForRemoval = props.modelValue.groups.find(
      (x: Group) => x.name === groupOption.name,
    );
    // TODO : Add error handling
    if (objForRemoval) {
      const index = props.modelValue.groups.indexOf(objForRemoval);
      props.modelValue.groups.splice(index, 1);
    }
  }
}

// Handle submission of form.
async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (props.newUserFlag) {
    if (props.modelValue.username.trim() === "") {
      formErrors.value.username = true;
      inputError = true;
    }

    // TODO : Bug fix this between edit and new user style
    if (
      props.modelValue.password == undefined ||
      props.modelValue.password.trim() === ""
    ) {
      formErrors.value.password = true;
      inputError = true;
    }
  }

  if (changePasswordFlag.value) {
    if (
      props.modelValue.password == undefined ||
      props.modelValue.password.trim() === ""
    ) {
      formErrors.value.password = true;
      inputError = true;
    }
    if (props.modelValue.password !== confirmPassword.value) {
      formErrors.value.confirmPassword = true;
      inputError = true;
    }
  }

  if (props.modelValue.role.trim() === "") {
    formErrors.value.role = true;
    inputError = true;
  }

  if (inputError) {
    inputErrorAlert();
    return;
  }
  emit("submit", props.modelValue);
}
</script>
