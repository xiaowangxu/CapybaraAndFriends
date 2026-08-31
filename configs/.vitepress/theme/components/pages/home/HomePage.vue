<script setup lang="ts">
import RecentArticles from './RecentArticles.vue'
</script>

<template>
  <main>
    <section class="h-100 flex flex-col justify-center items-center mt-24 pb-4 px-10">
      <div
        class="bg-[url('/assets/banner.png')] w-full flex-1 bg-contain bg-no-repeat bg-center">
      </div>
    </section>

    <section class="h-160 flex flex-col justify-center items-center mb-8">
      <RecentArticles />
    </section>
  </main>
</template>
