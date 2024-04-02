<template>
  <NuxtLayout name="base-layout">
    <div style="max-width: 30rem">
      <h1 class="section-header">Login to MLTE</h1>
      <UsaTextInput v-model="username" required type="text">
        <template #label> Username </template>
      </UsaTextInput>
      <UsaTextInput v-model="password" required type="password">
        <template #label> Password </template>
      </UsaTextInput>

      <div class="margin-button centered-container">
        <UsaButton class="primary-button" @click.prevent="submit()">
          Login
        </UsaButton>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();

const username = ref("");
const password = ref("");

async function submit() {
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

  try {
    await $fetch(config.public.apiPath + "/token", {
      retry: 0,
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formBody,
      onRequestError({ request }) {
        console.log(request);
        requestErrorAlert();
      },
      onResponse({ response }) {
        const token = useCookie("token", {
          Secure: true,
          maxAge: response?._data?.expires_in,
        });
        token.value = response?._data?.access_token;
        navigateTo("/");
      },
      onResponseError({ response }) {
        if (response.status === 400) {
          alert400Error(response._data.invalid_grant);
        } else if (response.status === 409) {
          conflictErrorAlert();
        } else {
          responseErrorAlert();
        }
      },
    });
  } catch (error) {
    console.log("Error in fetch.");
    console.log(error);
  }
}
</script>
