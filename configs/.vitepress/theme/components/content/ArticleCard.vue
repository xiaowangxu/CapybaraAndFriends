<script setup lang="ts">
import { ArrowUpRight, Clock3 } from '@lucide/vue'
import { withBase } from 'vitepress'
import { formatDate, type DocRecord } from '../../data/content'

const props = withDefaults(defineProps<{
  article: DocRecord
  index?: number
  featured?: boolean
}>(), {
  featured: false
})

const numberLabel = String((props.index ?? 0) + 1).padStart(2, '0')
</script>

<template>
  <a
    :href="withBase(article.url)"
    class="group block bg-transparent border border-transparent rounded-2xl px-8 py-6 transition duration-250 hover:bg-white hover:border-neutral-300 hover:shadow-2xl/5 hover:-translate-y-0.5"
  >
    <div class="grid grid-cols-[minmax(0,1fr)_auto] gap-x-4 gap-y-4 md:grid-cols-[8.5rem_minmax(0,1fr)_10.5rem] md:items-center md:gap-8">
      <div class="col-span-2 flex items-start justify-between self-start gap-2 md:col-span-1 md:block">
        <div v-if="index !== undefined">
          <span class="block text-lg">{{ numberLabel }}</span>
        </div>
        <time class="text-neutral-400 text-sm" :datetime="String(article.frontmatter.date || '')">
          {{ formatDate(article.frontmatter.date) }}
        </time>
      </div>

      <div class="col-span-2 min-w-0 md:col-span-1 flex flex-col gap-2">
        <h1 class="text-2xl font-[450]">
          {{ article.frontmatter.title || article.slug }}
        </h1>
        <p class="">
          {{ article.frontmatter.description || article.excerpt }}
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-neutral-400 md:col-span-1 md:block md:text-right">
        <span>{{ article.frontmatter.type || 'Research' }}</span>
        <span v-if="article.frontmatter.topic" aria-hidden="true">·</span>
        <span v-if="article.frontmatter.topic">{{ article.frontmatter.topic }}</span>
      </div>
    </div>
  </a>
</template>
