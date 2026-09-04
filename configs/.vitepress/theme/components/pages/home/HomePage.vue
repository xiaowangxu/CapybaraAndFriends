<script setup lang="ts">
import { computed } from 'vue'
import { useData, withBase } from 'vitepress'
import CardGrid from './CardGrid.vue'
import RecentArticles from './RecentArticles.vue'
import type { CardGridConfig } from './cards'

const { frontmatter } = useData()
const cardGrid = computed(() => frontmatter.value.cardGrid as CardGridConfig | undefined)

</script>

<template>
  <main>
    <section class="h-100 flex flex-col justify-center items-center mt-24 pb-4 px-10">
      <div class="w-full flex-1 bg-contain bg-no-repeat bg-center"
        :style="{ backgroundImage: `url(${withBase('/assets/banner.png')})` }">
      </div>
    </section>

    <section class="flex flex-col justify-center items-center max-w-7xl mx-auto mt-16 mb-10 px-6">
      <CardGrid v-if="cardGrid" :config="cardGrid" />
    </section>

    <section class="flex flex-col justify-center items-center">
      <RecentArticles />
    </section>
  </main>
</template>
