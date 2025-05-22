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

    <UsaTextInput v-model="user.email">
      <template #label> Email </template>
    </UsaTextInput>

    <UsaTextInput v-model="user.full_name">
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
const config = useRuntimeConfig();
const token = useCookie("token");
const userCookie = useCookie("user");

const { data: user } = await useFetch(config.public.apiPath + "/user/me", {
  retry: 0,
  method: "GET",
  headers: {
    Authorization: "Bearer " + token.value,
  },
});
const resetPasswordFlag = ref(false);
const newPassword = ref("");
const confirmPassword = ref("");
const formErrors = ref({
  password: false,
  confirmPassword: false,
});

function enablePasswordReset() {
  newPassword.value = "";
  confirmPassword.value = "";
  resetPasswordFlag.value = true;
}

function disablePasswordReset() {
  resetPasswordFlag.value = false;
  newPassword.value = "";
  confirmPassword.value = "";
}

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

  try {
    const requestBody = {
      username: user.value.username,
      email: user.value.email,
      full_name: user.value.full_name,
      disabled: false,
      role: user.value.role,
    };

    if (resetPasswordFlag.value) {
      requestBody.password = newPassword.value;
    }

    await $fetch(config.public.apiPath + "/user", {
      retry: 0,
      method: "PUT",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      body: requestBody,
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          navigateTo("/");
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    });
  } catch (exception) {
    console.log(exception);
  }
}
</script>
