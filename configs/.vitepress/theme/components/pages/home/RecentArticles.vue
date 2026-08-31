<script setup lang="ts">
import { computed } from 'vue'
import { ArrowRight, BookOpen, ChevronRight } from '@lucide/vue'
import { researchArticles } from '../../../data/content'
import { routes, siteText } from '../../../data/site'
import ArticleCard from '../../content/ArticleCard.vue'

const latest = computed(() => researchArticles().slice(0, 4))
</script>

<template>
  <section id="latest" class="home-section home-section--latest">
    <div class="section-heading-row">
      <div class="section-heading-row__title">
        <p class="section-label"><BookOpen :size="15" :stroke-width="1.8" />{{ siteText.home.latestLabel }}</p>
        <h2>{{ siteText.home.latest }}</h2>
      </div>
      <a :href="routes.research" class="text-link">{{ siteText.home.viewAll }}<ArrowRight :size="16" :stroke-width="1.8" /></a>
    </div>

    <div class="latest-layout">
      <aside class="section-rail panel">
        <!-- <div class="section-rail__top">
          <span class="status-dot" aria-hidden="true"></span>
          <span>{{ siteText.home.signal }}</span>
        </div>
        <div class="section-rail__count"><strong>{{ latest.length }}</strong><span>{{ siteText.home.recentCount }}</span></div>
        <div class="section-rail__topics">
          <span v-for="article in latest.slice(0, 3)" :key="article.url"><ChevronRight :size="14" :stroke-width="1.8" />{{ article.frontmatter.topic || article.frontmatter.type }}</span>
        </div> -->
      </aside>
      <div class="article-list">
        <ArticleCard v-for="(article, index) in latest" :key="article.url" :article="article" :featured="index === 0" />
      </div>
    </div>
  </section>
</template>
