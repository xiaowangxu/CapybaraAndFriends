<script setup lang="ts">
import { ArrowUpRight, GitBranch, Rss } from '@lucide/vue'
import { routes, siteText } from '../../data/site'

</script>

<template>
  <footer class="bg-neutral-900 px-20 py-6 flex justify-end gap-24 items-center">
    <a :href="routes.home" class="text-white! text-xl font-[Georgia] italic mr-auto">Capybara &amp; Friends</a>
    <div class="text-white flex gap-2">
      <a class="footer-link" href="https://github.com/" target="_blank" rel="noreferrer" aria-label="GitHub">
        <GitBranch :size="17" :stroke-width="1.8" />
        <span>GitHub</span>
      </a>
      <a class="footer-link" href="/feed.xml" aria-label="RSS">
        <Rss :size="17" :stroke-width="1.8" />
        <span>RSS</span>
      </a>
    </div>
  </footer>
</template>

<style scoped>
@reference "../../style.css";

.footer-link {
  @apply flex gap-2 items-center hover:bg-neutral-700 transition-colors px-3 py-2 rounded-xl;
}
</style>
