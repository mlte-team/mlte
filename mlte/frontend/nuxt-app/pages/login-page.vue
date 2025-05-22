<template>
  <NuxtLayout name="base-layout">
    <template #page-title>Login</template>
    <form>
      <div style="max-width: 30rem">
        <UsaTextInput v-model="username" :error="formErrors.username">
          <template #label> Username </template>
          <template #error-message> Enter a username </template>
        </UsaTextInput>
        <UsaTextInput
          v-model="password"
          :error="formErrors.password"
          type="password"
        >
          <template #label> Password </template>
          <template #error-message> Enter a password </template>
        </UsaTextInput>

        <div class="margin-button centered-container">
          <UsaButton
            type="submit"
            class="primary-button"
            @click.prevent="submit()"
          >
            Login
          </UsaButton>
        </div>
      </div>
    </form>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();

const username = ref("");
const password = ref("");

const formErrors = ref({
  username: false,
  password: false,
});

async function submit() {
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (username.value.trim() === "") {
    formErrors.value.username = true;
    inputError = true;
  }
  if (password.value.trim() === "") {
    formErrors.value.password = true;
    inputError = true;
  }

  if (inputError) {
    inputErrorAlert();
    return;
  }

  const details = {
    grant_type: "password",
    username: username.value,
    password: password.value,
  };

  let formBody = [];
  for (const property in details) {
    const encodedKey = encodeURIComponent(property);
    const encodedValue = encodeURIComponent(details[property]);
    formBody.push(encodedKey + "=" + encodedValue);
  }
  formBody = formBody.join("&");
  let expiresInTemp = 0;

  try {
    await $fetch(config.public.apiPath + "/token", {
      retry: 0,
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formBody,
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          expiresInTemp = response?._data?.expires_in;
          const token = useCookie("token", {
            maxAge: expiresInTemp,
          });
          const user = useCookie("user", {
            maxAge: expiresInTemp,
          });
          token.value = response?._data?.access_token;
          user.value = username.value;
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    });

    const token = useCookie("token");
    await $fetch(config.public.apiPath + "/user/me", {
      retry: 0,
      method: "GET",
      headers: {
        Authorization: "Bearer " + token.value,
      },
      onRequestError() {
        requestErrorAlert();
      },
      onResponse({ response }) {
        if (response.ok) {
          const userRole = useCookie("userRole", {
            maxAge: expiresInTemp,
          });
          userRole.value = response._data.role;
        }
      },
      onResponseError({ response }) {
        handleHttpError(response.status, response._data.error_description);
      },
    });

    navigateTo("/");
  } catch (exception) {
    console.log("Error in login: ");
    console.log(exception);
  }
}
</script>
