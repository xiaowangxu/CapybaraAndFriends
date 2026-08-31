<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from 'vue'
import { ArrowLeft, ArrowUpRight, BookOpen, Clock3 } from '@lucide/vue'
import { onContentUpdated, useData } from 'vitepress'
import { formatDate, researchArticles } from '../../data/content'
import { routes, siteText } from '../../data/site'

interface Heading { id: string; text: string; level: number }
const { frontmatter, page } = useData()
const headings = ref<Heading[]>([])
const text = siteText.article
const currentUrl = computed(() => {
  const relativePath = (page.value.relativePath || '').replace(/\\/g, '/').replace(/\.md$/, '')
  if (relativePath === 'index') return '/'
  if (relativePath.endsWith('/index')) return `/${relativePath.replace(/\/index$/, '')}/`
  return `/${relativePath}`
})
const related = computed(() => researchArticles().filter(article => article.url.replace(/\/+$/, '') !== currentUrl.value.replace(/\/+$/, '')).slice(0, 2))

function refreshHeadings() {
  nextTick(() => {
    headings.value = Array.from(document.querySelectorAll('.article-content h1, .article-content h2, .article-content h3')).map(element => ({
      id: element.id,
      text: element.textContent || '',
      level: Number(element.tagName.slice(1))
    }))
  })
}

onMounted(refreshHeadings)
onContentUpdated(refreshHeadings)
</script>

<template>
  <main class="article-page">

    <header class="mt-36 mb-20 px-10 flex">
      <div class="mx-auto flex flex-col items-center gap-5">
        <div class="flex gap-4 text-neutral-400 text-sm">
          <span v-if="frontmatter.author">{{ frontmatter.author }}</span>
          <time v-if="frontmatter.date" :datetime="String(frontmatter.date)">{{
            formatDate(frontmatter.date) }}</time>
        </div>
        <h1 class="text-5xl font-[450]">{{ frontmatter.title }}</h1>
        <p class="">{{ frontmatter.description }}</p>
        <!-- <a :href="routes.research" class="back-link"><ArrowLeft :size="16" :stroke-width="1.8" />{{ text.back }}</a> -->
        <!-- <div class="">
          <span class="article-type">{{ frontmatter.type || 'Research' }}</span>
          <span v-if="frontmatter.topic">{{ frontmatter.topic }}</span>
          <span v-if="frontmatter.status" class="meta-status"><span class="status-dot" aria-hidden="true"></span>{{
            frontmatter.status }}</span>
        </div> -->
      </div>
    </header>
    
    <!-- <aside class="fixed right-10">
      <div class="toc-card panel">
        <p class="panel-label">
          <BookOpen :size="15" :stroke-width="1.8" />{{ text.contents }}
        </p>
        <nav v-if="headings.length" class="toc-list">
          <a v-for="heading in headings" :key="heading.id" :href="`#${heading.id}`"
            :class="{ 'is-subheading': heading.level === 3 }">{{ heading.text }}</a>
        </nav>
        <p v-else class="toc-empty">{{ text.noSections }}</p>
      </div>
    </aside> -->

    <div class="max-w-4xl px-10 mx-auto">
      <article class="article-content">
        <slot />
      </article>
    </div>

    <section v-if="related.length" class="related-section page-container">
      <div class="related-section__heading">
        <p class="section-label">
          <ArrowUpRight :size="15" :stroke-width="1.8" />{{ text.related }}
        </p>
      </div>
      <div class="related-list">
        <a v-for="article in related" :key="article.url" :href="article.url" class="related-item">
          <div>
            <span>{{ article.frontmatter.type || 'Research' }}<span v-if="article.frontmatter.topic"> · {{
              article.frontmatter.topic }}</span></span>
            <h2>{{ article.frontmatter.title }}</h2>
          </div>
          <ArrowUpRight :size="18" :stroke-width="1.8" />
        </a>
      </div>
    </section>
  </main>
</template>
