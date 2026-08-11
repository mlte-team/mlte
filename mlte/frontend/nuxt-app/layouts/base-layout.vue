<template>
  <div class="page-container">
    <div style="height: 16px; background-color: #f3ca3e" />
    <header class="header-container">
      <NuxtLink to="/" class="header-link">
        <img
          src="~/assets/img/MLTE_Logo_Color.svg"
          height="75px"
          width="75px"
        />

        <div class="header-main">MLTE</div>
        <div class="header-secondary">
          Machine Learning <br />
          Test and Evaluation {{ route.name }}
        </div>
      </NuxtLink>
    </header>

    <div class="main-container">
      <aside class="sidebar-container">
        <div v-if="route.name != 'login'">
          <nav>
            <ul class="usa-sidenav">
              <li class="usa-sidenav__item">
                <NuxtLink
                  :to="{ path: '/' }"
                  :class="{
                    'usa-current': [
                      'index',
                      'artifact-negotiation-card',
                      'artifact-report-view',
                      'artifact-artifact-compare',
                      'artifact-suite-view',
                      'artifact-evidence-view',
                      'artifact-results-view',
                    ].includes(route.name as string),
                  }"
                >
                  Artifact Store
                </NuxtLink>
              </li>
              <li class="usa-sidenav__item">
                <NuxtLink
                  :to="{ path: '/catalog' }"
                  :class="{
                    'usa-current': route.name === 'catalog',
                  }"
                  @click="$emit('nav')"
                >
                  Test Catalog
                </NuxtLink>
              </li>
              <li class="usa-sidenav__item">
                <NuxtLink
                  :to="{ path: '/custom-list' }"
                  :class="{
                    'usa-current': route.name === 'custom-list',
                  }"
                  @click="$emit('nav')"
                >
                  Custom Lists
                </NuxtLink>
              </li>
              <li class="usa-sidenav__item">
                <NuxtLink
                  :to="{ path: '/etc/quality-model' }"
                  :class="{
                    'usa-current': route.name === 'etc-quality-model',
                  }"
                  @click="$emit('nav')"
                >
                  Quality Model
                </NuxtLink>
              </li>
              <li v-if="userRole === 'admin'" class="usa-sidenav__item">
                <div class="nav-section-title">Admin Pages</div>
                <ul class="usa-sidenav__sublist">
                  <li class="usa-sidenav__item">
                    <NuxtLink
                      :to="{ path: '/admin/manage-users' }"
                      :class="{
                        'usa-current': route.name === 'admin-manage-users',
                      }"
                      @click="$emit('nav')"
                    >
                      Manage Users
                    </NuxtLink>
                  </li>
                  <li class="usa-sidenav__item">
                    <NuxtLink
                      :to="{ path: '/admin/manage-groups' }"
                      :class="{
                        'usa-current': route.name === 'admin-manage-groups',
                      }"
                      @click="$emit('nav')"
                    >
                      Manage Groups
                    </NuxtLink>
                  </li>
                </ul>
              </li>
              <li v-else class="usa-sidenav__item">
                <div class="nav-section-title">User Pages</div>
                <ul class="usa-sidenav__sublist">
                  <li class="usa-sidenav__item">
                    <NuxtLink
                      :to="{ path: '/regular/profile-edit' }"
                      :class="{
                        'usa-current': route.name === 'regular-profile-edit',
                      }"
                    >
                      Edit Profile
                    </NuxtLink>
                  </li>
                </ul>
              </li>
            </ul>
          </nav>
          <div class="sidebar-slot-container">
            <slot name="left-sidebar" />
          </div>
        </div>
      </aside>

      <div class="body-container">
        <div class="header-row">
          <h1 class="section-header" style="margin: 0px;">
            <slot name="page-title" />
          </h1>
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
            </div>
          </div>
        </div>
        <hr />
        <slot name="default" />
      </div>
    </div>

    <footer>
      <p>
        <b>MLTE - {{ currentDate.getFullYear() }}</b>
      </p>
      <div>
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
import { confirmLogout } from "~/composables/auth";

const emits = defineEmits(["nav"]);

const config = useRuntimeConfig();
const route = useRoute();
const token = useCookie("token");
const user = useCookie("user");
const userRole = useCookie("userRole");
const version = config.public.version;

const currentDate = new Date();
</script>

<style>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header-container {
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

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logout-header {
  display: flex;
  align-items: center;
}

.main-container {
  display: flex;
  width: 100%;
  flex: 1;
}

.sidebar-container {
  width: 30ch;
  min-width: 30ch;
  padding-top: 60px;
  margin-left: 30px;

  position: sticky;
  top: 20px;
  align-self: flex-start;
  height: fit-content;
}

.sidebar-slot-container {
  padding-top: 1rem;
}

.nav-section-title {
  padding: 0.5rem 1rem;
  display: block;
  color: #565c65;
}

.body-container {
  flex: 1;
  min-width: 0;
  max-width: 128ch;
  margin-top: 8px;
  margin-left: 40px;
  padding-right: 40px;
}

footer {
  min-height: 90px;
  padding: 20px 40px 0;
  font-size: 16px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

footer > div > a,
footer > div > span {
  margin-left: 30px;
}
</style>
