// https://vitepress.dev/guide/custom-theme
import Layout from './Layout.vue'
import type { Theme } from 'vitepress'
import './style.css'

export default {
  Layout,
  enhanceApp({ app }) {
    if (!import.meta.env.SSR) {
      import('shader-doodle')
    }
  }
} satisfies Theme

