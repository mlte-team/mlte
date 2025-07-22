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
const username = ref("");
const password = ref("");

const formErrors = ref<Dictionary<boolean>>({
  username: false,
  password: false,
});

// Handle submission of form.
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

  const details: Dictionary<string> = {
    grant_type: "password",
    username: username.value,
    password: password.value,
  };

  const formBodyArray: Array<string> = [];
  for (const property in details) {
    const encodedKey = encodeURIComponent(property);
    const encodedValue = encodeURIComponent(details[property]);
    formBodyArray.push(encodedKey + "=" + encodedValue);
  }
  const formBodyStr: string = formBodyArray.join("&");
  let expiresInTemp = 0;

  const tokenData: TokenData | null = await useApi(
    "/token",
    "POST",
    {
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formBodyStr,
    },
    undefined,
    false,
  );

  if (tokenData) {
    expiresInTemp = tokenData.expires_in;
    const token = useCookie("token", {
      maxAge: tokenData.expires_in,
    });
    const user = useCookie("user", {
      maxAge: expiresInTemp,
    });
    token.value = tokenData.access_token;
    user.value = username.value;

    const userData: User | null = await useApi(
      "/user/me",
      "GET",
      undefined,
      token.value as string,
    );
    if (userData) {
      const userRole = useCookie("userRole", {
        maxAge: expiresInTemp,
      });
      userRole.value = userData.role;
    }
  }

  navigateTo("/");
}
</script>
