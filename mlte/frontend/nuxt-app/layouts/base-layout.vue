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
      <div class="sidebar left-sidebar">
        <div style="position: fixed">
          <div v-if="route.name != 'login'" class="grid-row grid-gap">
            <div
              class="tablet:grid-col-4 margin-bottom-4 tablet:margin-bottom-0"
            >
              <nav aria-label="Side navigation,">
                <ul class="usa-sidenav" style="width: 30ch">
                  <li class="usa-sidenav__item">
                    <NuxtLink
                      :to="{ path: '/' }"
                      :class="{ 'usa-current': route.name === 'index' }"
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
                            'usa-current':
                              route.name === 'regular-profile-edit',
                          }"
                        >
                          Edit Profile
                        </NuxtLink>
                      </li>
                    </ul>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>

      <div class="body-div">
        <h1
          class="section-header"
          style="display: inline; align-items: left; justify-content: left"
        >
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
        <hr />
        <slot name="default" />
        <footer>
          <p class="footer-text-left">
            <b>MLTE - {{ currentDate.getFullYear() }}</b>
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

      <div class="sidebar">
        <div class="right-sidebar">
          <slot name="right-sidebar" />
        </div>
      </div>
    </div>
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
  float: right;
}

.flex-container {
  display: flex;
}

.sidebar {
  width: 100%;
  max-width: 30ch;
  padding-top: 60px;
}

.left-sidebar {
  margin-left: 30px;
}

.right-sidebar {
  margin-right: 40px;
  position: fixed;
}

.nav-section-title {
  padding: 0.5rem 1rem;
  display: block;
  color: #565c65;
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
  margin-top: 15px;
  bottom: 0;
  left: 0;
  font-size: 16px;
}

.footer-text-left {
  float: left;
}

.footer-text-right {
  margin-top: 20px;
  float: right;
}

footer > div > a,
footer > div > span {
  margin-left: 30px;
}
</style>
