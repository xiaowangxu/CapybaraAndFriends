// https://vitepress.dev/guide/custom-theme
import Layout from './Layout.vue'
import type { Theme } from 'vitepress'
import ResearchFigure from './components/research/ResearchFigure.vue'
import CalloutBlock from './components/research/CalloutBlock.vue'
import InteractiveFigure from './components/research/InteractiveFigure.vue'
import './style.css'

export default {
  Layout,
  enhanceApp({ app }) {
    app.component('ResearchFigure', ResearchFigure)
    app.component('KeyIdea', CalloutBlock)
    app.component('ResearchNote', CalloutBlock)
    app.component('InteractiveFigure', InteractiveFigure)
  }
} satisfies Theme

