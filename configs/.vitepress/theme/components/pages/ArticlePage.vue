<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from 'vue'
import { ArrowLeft, ArrowUpRight, BookOpen, ChevronDown, Clock3 } from '@lucide/vue'
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

    <header class="mt-24 mb-16 px-5 flex sm:mt-36 sm:mb-26 sm:px-10">
      <div class="mx-auto flex flex-col items-center gap-4 sm:gap-5">
        <div class="flex gap-4 text-xs text-neutral-400 sm:text-sm">
          <span v-if="frontmatter.author">{{ frontmatter.author }}</span>
          <time v-if="frontmatter.date" :datetime="String(frontmatter.date)">{{
            formatDate(frontmatter.date) }}</time>
        </div>
        <h1 class="text-center text-3xl leading-tight font-[450] sm:text-5xl">{{ frontmatter.title }}</h1>
        <p class="max-w-2xl text-center text-sm leading-relaxed sm:text-base">{{ frontmatter.description }}</p>
        <!-- <a :href="routes.research" class="back-link"><ArrowLeft :size="16" :stroke-width="1.8" />{{ text.back }}</a> -->
        <!-- <div class="">
          <span class="article-type">{{ frontmatter.type || 'Research' }}</span>
          <span v-if="frontmatter.topic">{{ frontmatter.topic }}</span>
          <span v-if="frontmatter.status" class="meta-status"><span class="status-dot" aria-hidden="true"></span>{{
            frontmatter.status }}</span>
        </div> -->
      </div>
    </header>

    <div class="max-w-5xl px-5 mx-auto mb-24 sm:px-10 sm:mb-34">
      <details v-if="headings.length"
        class="group mb-12 overflow-hidden rounded-2xl bg-white outline outline-neutral-300 shadow-lg/5 sm:hidden">
        <summary
          class="flex cursor-pointer items-center gap-2 px-4 py-3.5 text-sm font-medium text-neutral-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[var(--cf-accent)]">
          <BookOpen :size="16" :stroke-width="1.8" />
          {{ text.contents }}
          <ChevronDown :size="16" :stroke-width="1.8" class="ml-auto transition-transform group-open:rotate-180" />
        </summary>
        <nav class="flex flex-col border-t border-neutral-200 px-2 py-2" :aria-label="text.contents">
          <a v-for="heading in headings" :key="heading.id" :href="`#${heading.id}`"
            class="flex min-w-0 items-start rounded-xl py-2 pr-3 text-sm leading-snug text-neutral-700! active:bg-neutral-100"
            :style="{ paddingLeft: `${0.75 + (Math.min(3, heading.level) - 1) * 0.75}rem` }">
            <span class="mt-1.5 mr-2.5 size-1.5 shrink-0 rounded-full"
              :class="heading.level === 1 ? 'bg-amber-400' : 'bg-neutral-200'"></span>
            <span class="min-w-0 break-words">{{ heading.text }}</span>
          </a>
        </nav>
      </details>

      <article class="article-content">
        <slot />
      </article>
    </div>

    <div class="fixed right-0 top-0 bottom-0 hidden flex-col justify-center items-end py-6 sm:flex">
      <div class="p-10 overflow-hidden group">
        <aside class="bg-white outline outline-neutral-300 shadow-lg/5 flex gap-2 overflow-y-auto overflow-x-hidden px-2 py-2 box-content max-h-full scrollbar-none
        w-8 rounded-2xl group-hover:w-80 transition-all duration-200">
          <nav v-if="headings.length" class="flex w-full min-w-0 flex-col gap-0 min-h-fit">
            <a v-for="heading in headings" :key="heading.id" :href="`#${heading.id}`"
              class="block w-full min-w-0 rounded-xl hover:bg-neutral-100 text-neutral-800! hover:text-black! transition-colors pr-3">
              <div class="flex min-w-0 items-center text-sm py-0 text-inherit group-hover:py-1.5 transition-all duration-200"
                :class="[`group-hover:pl-${2 + (Math.min(3, heading.level) - 1) * 3}`]">
                <div class="flex shrink-0 justify-center w-4 mr-2.5">
                  <div class="aspect-square rounded-full"
                    :class="[heading.level === 1 ? 'bg-amber-400 w-1.75' : 'bg-neutral-200 w-1.25']"></div>
                </div>
                <span class="min-w-0 truncate opacity-0 group-hover:opacity-100 transition-all duration-100">{{ heading.text }}</span>
              </div>
            </a>
          </nav>
          <p v-else class="toc-empty">{{ text.noSections }}</p>
        </aside>
      </div>
    </div>

    <!-- <section v-if="related.length" class="related-section page-container">
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
    </section> -->
  </main>
</template>
