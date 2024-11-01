import pkg from "./package.json";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  typescript: {
    strict: true,
  },

  ssr: false,
  css: ["@/assets/css/styles.css", "@/assets/uswds/css/styles.css"],

  runtimeConfig: {
    public: {
      apiPath: "", // Overwritten by `mlte/frontend/nuxt-app/.env`
      version: pkg.version,
    },
  },
});