<template>
  <NuxtLayout name="base-layout">
    <title>Edit Profile</title>
    <template #page-title>Edit Profile</template>
    <h2 class="section-header" style="display: inline">
      {{ userCookie }}
    </h2>
    <UsaButton
      v-if="!resetPasswordFlag"
      class="secondary-button sub-header-float-button"
      @click="enablePasswordReset"
    >
      Change Password
    </UsaButton>
    <UsaButton
      v-if="resetPasswordFlag"
      class="secondary-button sub-header-float-button"
      @click="disablePasswordReset"
    >
      Cancel Change
    </UsaButton>
    <div v-if="resetPasswordFlag">
      <UsaTextInput
        v-model="newPassword"
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

    <UsaTextInput v-model="user!.email">
      <template #label> Email </template>
    </UsaTextInput>

    <UsaTextInput v-model="user!.full_name">
      <template #label> Full Name </template>
    </UsaTextInput>

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { cancelFormSubmission } from "~/composables/form-methods";

const userCookie = useCookie("user");

const user = ref<User>(new User());
user.value = (await useApi("/user/me", "GET")) || new User();

const resetPasswordFlag = ref(false);
const newPassword = ref("");
const confirmPassword = ref("");
const formErrors = ref<Dictionary<boolean>>({
  password: false,
  confirmPassword: false,
});

// Enables the password and confirm password form fields.
function enablePasswordReset() {
  newPassword.value = "";
  confirmPassword.value = "";
  resetPasswordFlag.value = true;
}

// Disables the password and confirm password form fields.
function disablePasswordReset() {
  resetPasswordFlag.value = false;
  newPassword.value = "";
  confirmPassword.value = "";
}

// Handle submission of form.
async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (resetPasswordFlag.value) {
    if (newPassword.value.trim() === "") {
      formErrors.value.password = true;
      inputError = true;
    }
    if (newPassword.value !== confirmPassword.value) {
      formErrors.value.confirmPassword = true;
      inputError = true;
    }
  }

  if (inputError) {
    inputErrorAlert();
    return;
  }

  const requestBody: UserUpdateBody = {
    username: user.value!.username,
    email: user.value!.email,
    full_name: user.value!.full_name,
    disabled: false,
    role: user.value!.role,
  };

  if (resetPasswordFlag.value) {
    requestBody.password = newPassword.value;
  }

  const response = await useApi("/user", "PUT", {
    body: requestBody,
  });
  if (response) {
    navigateTo("/");
  }
}
</script>
