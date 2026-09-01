<script setup lang="ts">
import { withBase } from 'vitepress'
import { routes, siteText } from '../../data/site'
import BrandMark from '../ui/BrandMark.vue'

const links = [
  { label: siteText.nav.research, href: routes.research },
  // { label: siteText.nav.about, href: routes.about }
]
</script>

<template>
  <header class="px-10 pt-6 pb-4 fixed top-0 flex z-100">
    <div class="bg-white border border-neutral-300 rounded-full shadow-lg/5
    flex pl-4.5 py-2 pr-2 gap-2">
      <a :href="withBase(routes.home)" class="max-w-fit inline-flex" aria-label="Capybara & Friends">
        <BrandMark />
      </a>
      <nav class="site-nav" aria-label="主导航">
        <a v-for="link in links" :key="link.href" :href="withBase(link.href)">{{ link.label }}</a>
      </nav>
    </div>
  </header>
</template>

<style scoped>
@reference '../../style.css';

.site-nav {
  @apply flex items-center mr-auto;
}

.site-nav a {
  @apply rounded-full px-3 h-full text-sm 
  flex justify-center items-center
  text-neutral-800 hover:text-black hover:bg-neutral-100
  transition-colors;
}

</style>
