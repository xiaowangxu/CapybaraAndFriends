<script setup lang="ts">
import { ArrowUpRight, GitBranch, Rss } from '@lucide/vue'
import { routes, siteText } from '../../data/site'

</script>

<template>
  <footer class="bg-neutral-900 px-20 py-6 flex justify-end gap-24 items-center">
    <a :href="routes.home" class="text-white! text-xl font-[Georgia] italic mr-auto">Capybara &amp; Friends</a>
    <!-- <divx -->
  </footer>
</template>

<style scoped>
@reference "../../style.css";

.footer-link {
  @apply flex gap-2 items-center hover:bg-neutral-700 transition-colors px-3 py-2 rounded-xl;
}
</style>
