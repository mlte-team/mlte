import VueUswds from "vue-uswds";
// const VueUswds = require("vue-uswds");

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VueUswds);
});
