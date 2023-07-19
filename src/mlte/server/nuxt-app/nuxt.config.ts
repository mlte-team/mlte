// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    target: 'static',

    css: [
        '@/assets/css/styles.css',
        '@/assets/uswds/css/styles.css'
    ],

    routeRules: {
        '/proxy/**': { proxy: 'http://localhost:8080/api/**'}
    }
})