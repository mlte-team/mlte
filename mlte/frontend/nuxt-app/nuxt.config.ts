import pkg from "./package.json";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  typescript: {
    strict: true,
  },

  ssr: false,
  css: ["@/assets/uswds/css/styles.css", "@/assets/css/styles.css"],

  runtimeConfig: {
    public: {
      apiPath: "http://localhost:8080/api",
      version: pkg.version,
    },
  },

  modules: ["@nuxt/eslint"],
});
