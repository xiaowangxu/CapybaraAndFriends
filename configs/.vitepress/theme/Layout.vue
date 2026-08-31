<script setup lang="ts">
import { useData } from 'vitepress'
import SiteHeader from './components/layout/SiteHeader.vue'
import SiteFooter from './components/layout/SiteFooter.vue'
import HomePage from './components/pages/home/HomePage.vue'
import ArticlePage from './components/pages/ArticlePage.vue'
import ContentPage from './components/pages/ContentPage.vue'

const { frontmatter } = useData()
</script>

<template>
  <SiteHeader />
  <div class="site-frame">
    <div class="site-main">
      <HomePage v-if="frontmatter.layout === 'home'" />
      <ArticlePage v-else-if="frontmatter.layout === 'article'">
        <Content />
      </ArticlePage>
      <ContentPage v-else>
        <Content />
      </ContentPage>
    </div>
    <SiteFooter />
  </div>
</template>
