<script setup lang="ts">
import { computed, ref } from 'vue'
import { ChevronDown, FileText, Search, X } from '@lucide/vue'
import { useData } from 'vitepress'
import { researchArticles } from '../../data/content'
import { siteText } from '../../data/site'
import ArticleCard from '../layout/ArticleCard.vue'

const { frontmatter } = useData()
const articles = researchArticles()
const query = ref('')
const selectedTopic = ref('all')

const topics = computed(() => Array.from(new Set(
  articles
    .map(article => String(article.frontmatter.topic || '').trim())
    .filter(Boolean)
)))

const filteredArticles = computed(() => {
  const normalizedQuery = query.value.trim().toLocaleLowerCase()

  return articles.filter(article => {
    const topic = String(article.frontmatter.topic || '')
    const searchableText = [
      article.frontmatter.title,
      article.frontmatter.description,
      article.frontmatter.type,
      topic
    ].filter(Boolean).join(' ').toLocaleLowerCase()

    return (selectedTopic.value === 'all' || topic === selectedTopic.value)
      && (!normalizedQuery || searchableText.includes(normalizedQuery))
  })
})

const hasFilters = computed(() => Boolean(query.value.trim()) || selectedTopic.value !== 'all')
const pageTitle = computed(() => frontmatter.value.title || siteText.research.title)
const pageDescription = computed(() => frontmatter.value.description || siteText.research.description)

function clearFilters() {
  query.value = ''
  selectedTopic.value = 'all'
}
</script>

<template>
  <main class="overflow-hidden">
    <div class="mx-auto w-full max-w-7xl px-10 mt-36 mb-34 flex flex-col">
      <header class="flex flex-col items-start gap-5 pl-8 mb-11">
        <h1 class="text-5xl font-[450]">
          {{ pageTitle }}
        </h1>
        <p class="">
          {{ pageDescription }}
        </p>
      </header>

      <!-- <section class="mt-12" aria-label="研究筛选">
        <div class="flex flex-col gap-3 border-y border-[#dedede] py-4 sm:flex-row sm:items-center">
          <label class="relative min-w-0 flex-1">
            <span class="sr-only">{{ siteText.research.search }}</span>
            <Search class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#766d68]" :size="17" :stroke-width="1.8" aria-hidden="true" />
            <input
              v-model="query"
              type="search"
              :placeholder="siteText.research.search"
              class="h-12 w-full rounded-xl border border-[#d9d4d1] bg-white/60 pl-11 pr-4 text-sm text-black outline-none transition-colors placeholder:text-[#9a9390] hover:border-[#b9aaa2] focus:border-[#2d1e17] focus:ring-2 focus:ring-[#2d1e17]/10 sm:text-base"
            />
          </label>

          <label class="relative w-full sm:w-44">
            <span class="sr-only">{{ siteText.research.filter }}</span>
            <select
              v-model="selectedTopic"
              class="h-12 w-full appearance-none rounded-xl border border-[#d9d4d1] bg-white/60 px-4 pr-10 text-sm text-black outline-none transition-colors hover:border-[#b9aaa2] focus:border-[#2d1e17] focus:ring-2 focus:ring-[#2d1e17]/10 sm:text-base"
            >
              <option value="all">{{ siteText.research.all }}</option>
              <option v-for="topic in topics" :key="topic" :value="topic">{{ topic }}</option>
            </select>
            <ChevronDown class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-[#766d68]" :size="17" :stroke-width="1.8" aria-hidden="true" />
          </label>
        </div>

        <div class="flex min-h-12 flex-wrap items-center justify-between gap-3 py-4">
          <p class="text-sm text-[#766d68]">
            <span class="font-medium text-black">{{ filteredArticles.length }}</span>
            {{ siteText.research.results }}
          </p>
          <button
            v-if="hasFilters"
            type="button"
            class="inline-flex items-center gap-1.5 text-sm text-[#2d1e17] underline decoration-[#cdbdb3] underline-offset-4 transition-colors hover:text-[#8f6e5c] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#2d1e17]"
            @click="clearFilters"
          >
            <X :size="15" :stroke-width="1.8" aria-hidden="true" />
            {{ siteText.research.clearFilters }}
          </button>
        </div>
      </section> -->

      <section aria-label="文章列表">
        <div v-if="filteredArticles.length" class="space-y-1">
          <ArticleCard
            v-for="(article, index) in filteredArticles"
            :key="article.url"
            :article="article"
          />
        </div>

        <div v-else class="border-y border-[#dedede] py-16 text-center sm:py-20">
          <p class="text-base text-[#6f6965]">{{ siteText.research.noResults }}</p>
          <button
            type="button"
            class="mt-5 text-sm text-[#2d1e17] underline decoration-[#cdbdb3] underline-offset-4 transition-colors hover:text-[#8f6e5c] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#2d1e17]"
            @click="clearFilters"
          >
            {{ siteText.research.clearFilters }}
          </button>
        </div>
      </section>
    </div>
  </main>
</template>
