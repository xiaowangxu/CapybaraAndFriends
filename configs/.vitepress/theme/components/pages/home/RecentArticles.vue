<script setup lang="ts">
import { computed } from 'vue'
import { ArrowRight, BookOpen } from '@lucide/vue'
import { withBase } from 'vitepress'
import { researchArticles } from '../../../data/content'
import { routes, siteText } from '../../../data/site'
import ArticleCard from '../../layout/ArticleCard.vue'

const latest = computed(() => researchArticles().slice(0, 4))
</script>

<template>
  <section id="latest" class="mx-auto w-full max-w-7xl mt-16 mb-28 px-10">
    <div class="mb-10 flex items-end justify-between gap-6 px-8 pr-3.5">
      <div>
        <h2 class="mt-2 text-5xl font-[450]">
          {{ siteText.home.latest }}
        </h2>
      </div>
      <a
        :href="withBase(routes.research)"
        class="group inline-flex shrink-0 items-center gap-2 text-lg hover:bg-neutral-200 transition-colors px-4 py-2 rounded-xl"
      >
        {{ siteText.home.viewAll }}
        <ArrowRight :size="20" :stroke-width="1.5" class="transition-transform duration-300 group-hover:translate-x-1" aria-hidden="true" />
      </a>
    </div>

    <div>
      <ArticleCard
        v-for="(article, index) in latest"
        :key="article.url"
        :article="article"
        :index="index"
      />
    </div>
  </section>
</template>
