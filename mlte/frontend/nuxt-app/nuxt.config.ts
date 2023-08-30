// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  typescript: {
    strict: true,
  },
  ssr: false,
  css: ["@/assets/css/styles.css", "@/assets/uswds/css/styles.css"],
  nitro: {
    routeRules: {
      "/api/**": { proxy: "http://localhost:8080/api/**" },
    },
  }
});
