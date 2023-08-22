import { ComputedRef, Ref } from 'vue'
export type LayoutKey = "base-layout"
declare module "/Users/krmaffey/node_modules/nuxt/dist/pages/runtime/composables" {
  interface PageMeta {
    layout?: false | LayoutKey | Ref<LayoutKey> | ComputedRef<LayoutKey>
  }
}