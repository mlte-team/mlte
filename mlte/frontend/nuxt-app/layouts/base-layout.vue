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
        <div style="position: fixed;">
          <div v-if="$route.name != 'login'" class="grid-row grid-gap">
            <div class="tablet:grid-col-4 margin-bottom-4 tablet:margin-bottom-0">
              <nav aria-label="Side navigation,">
                <ul class="usa-sidenav" style="width: 30ch">
                  <li class="usa-sidenav__item">
                    <NuxtLink
                      :to="{ path: '/' }"
                      :class="{ 'usa-current': $route.name === 'index' }"
                    >
                      Artifact Store
                    </NuxtLink>
                  </li>
                  <li class="usa-sidenav__item">
                    <NuxtLink 
                      :to="{ path: '/test-catalog' }"
                      :class="{ 'usa-current': $route.name === 'test-catalog' }"
                    >
                      Test Catalog
                    </NuxtLink>
                  </li>
                  <li v-if="userRole === 'admin'" class="usa-sidenav__item">
                    <a href="javascript:void(0);">Admin Pages</a>
                    <ul class="usa-sidenav__sublist">
                      <li class="usa-sidenav__item">
                        <NuxtLink
                          :to="{ path: '/admin/user-management' }"
                          :class="{
                            'usa-current':
                              $route.name === 'admin-user-management',
                          }"
                        >
                          Manage Users
                        </NuxtLink>
                      </li>
                      <li class="usa-sidenav__item">
                        <NuxtLink
                          :to="{ path: '/admin/group-management' }"
                          :class="{
                            'usa-current':
                              $route.name === 'admin-group-management',
                          }"
                        >
                          Manage Groups
                        </NuxtLink>
                      </li>
                    </ul>
                  </li>
                  <li v-else class="usa-sidenav__item">
                    <a href="javascript:void(0);">User Pages</a>
                    <ul class="usa-sidenav__sublist">
                      <li class="usa-sidenav__item">
                        <NuxtLink
                          :to="{ path: '/regular/profile-edit' }"
                          :class="{
                            'usa-current': $route.name === 'regular-profile-edit',
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
        <slot name="default" />
      </div>

      <div class="sidebar">
        <div class="right-sidebar">
          <slot name="right-sidebar" />
        </div>
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
const userRole = useCookie("userRole");
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
  padding-top: 60px;
}

.left-sidebar {
  margin-left: 30px;
}

.right-sidebar {
  margin-right: 40px;
  position: fixed;
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
