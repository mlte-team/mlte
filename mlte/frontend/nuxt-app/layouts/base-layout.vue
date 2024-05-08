<template>
  <div>
    <div style="height: 16px; background-color: #f3ca3e" />
    <header class="flex-container">
      <a href="/" class="header-link">
        <img
          src="~/assets/img/MLTE_Logo_Color.svg"
          height="75px"
          width="75px"
        />

        <div class="header-main">MLTE</div>
        <div class="header-secondary">
          Machine Learning <br />
          Test and Evaluation
        </div>
      </a>
    </header>

    <div class="flex-container">
      <div class="sidebar">
        <slot name="sidebar" />
      </div>

      <div class="body-div">
        <div v-if="token" class="logout-header">
          <div class="centered-container">
            Welcome, {{ user }}
            <UsaButton
              class="secondary-button"
              style="margin-left: 0.5em"
              @click.prevent="confirmLogout()"
            >
              Logout
            </UsaButton>
            <NuxtLink :to="{ path: 'user-management' }">
              <UsaButton class="secondary-button" style="margin-left: 0.5em">
                Manage Users
              </UsaButton>
            </NuxtLink>
          </div>
        </div>
        <slot name="default" />
      </div>
    </div>

    <footer>
      <p class="footer-text-left">
        <b>MLTE - 2024</b>
      </p>
      <div class="footer-text-right">
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/mlte-team/mlte"
          >Github</a
        >
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://mlte.readthedocs.io/en/latest/"
          >Docs</a
        >
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://mlte.readthedocs.io/en/latest/using_mlte/"
          >User Guide</a
        >
        <span>v{{ version }}</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const token = useCookie("token");
const user = useCookie("user");
const version = config.public.version;
</script>

<style>
header {
  display: inline-block;
  margin-bottom: 8px;
  padding: 25px;
  background-color: #000000;
}

.header-main {
  display: inline-block;
  font-size: 56px;
  margin-right: 8px;
  vertical-align: top;
}

.header-secondary {
  display: inline-block;
  font-size: 24px;
  padding-top: 5px;
  vertical-align: top;
}

.header-link {
  color: white;
  text-decoration: none;
}

.logout-header {
  display: flex;
  align-items: right;
  justify-content: right;
}

.flex-container {
  display: flex;
}

.sidebar {
  width: 100%;
  max-width: 30ch;
  margin-left: 40px;
}

.body-div {
  width: 100%;
  max-width: 128ch;
  margin-top: 8px;
  margin-left: 40px;
  padding-right: 40px;
}

footer {
  width: 100%;
  height: 90px;
  margin-top: 8px;
  bottom: 0;
  left: 0;
  font-size: 16px;
}

.footer-text-left {
  margin-left: 40px;
  float: left;
}

.footer-text-right {
  margin-right: 40px;
  margin-top: 20px;
  float: right;
}

footer > div > a,
footer > div > span {
  margin-left: 30px;
}
</style>
