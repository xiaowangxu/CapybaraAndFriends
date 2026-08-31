<script setup lang="ts">
import { ArrowUpRight, Clock3 } from '@lucide/vue'
import { formatDate, type DocRecord } from '../../data/content'
import { siteText } from '../../data/site'

const props = withDefaults(defineProps<{
  article: DocRecord
  featured?: boolean
}>(), {
  featured: false
})
</script>

<template>
  <a :href="article.url" class="article-card" :class="{ 'article-card--featured': props.featured }">
    <div class="article-card__date">
      <time :datetime="String(article.frontmatter.date || '')">{{ formatDate(article.frontmatter.date) }}</time>
      <span v-if="props.featured" class="article-card__signal">{{ siteText.home.featured }}</span>
    </div>
    <div class="article-card__body">
      <div class="article-card__meta">
        <span>{{ article.frontmatter.type || 'Research' }}</span>
        <span v-if="article.frontmatter.topic">{{ article.frontmatter.topic }}</span>
      </div>
      <h3>{{ article.frontmatter.title || article.slug }}</h3>
      <p>{{ article.frontmatter.description || article.excerpt }}</p>
    </div>
    <div class="article-card__tail">
      <span v-if="article.frontmatter.readingTime" class="article-card__reading"><Clock3 :size="14" :stroke-width="1.8" />{{ article.frontmatter.readingTime }}</span>
      <ArrowUpRight :size="18" :stroke-width="1.8" aria-hidden="true" />
    </div>
  </a>
</template>
