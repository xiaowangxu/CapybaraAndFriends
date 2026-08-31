<script setup lang="ts">
import { withBase } from 'vitepress'
import RecentArticles from './RecentArticles.vue'
</script>

<template>
  <main>
    <section class="h-100 flex flex-col justify-center items-center mt-24 pb-4 px-10">
      <div
        class="w-full flex-1 bg-contain bg-no-repeat bg-center"
        :style="{ backgroundImage: `url(${withBase('/assets/banner.png')})` }">
      </div>
    </section>

    <section class="flex flex-col justify-center items-center">
      <RecentArticles />
    </section>
  </main>
</template>
