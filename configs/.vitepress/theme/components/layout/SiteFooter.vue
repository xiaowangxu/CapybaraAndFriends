<script setup lang="ts">
import { ArrowUpRight, GitBranch, Mail, Rss } from '@lucide/vue'
import { withBase } from 'vitepress'
import { routes, siteText } from '../../data/site'

const extraLinks = [
  { label: siteText.nav.github, href: routes.github, color: '#1f2328', icon: GitBranch },
  { label: siteText.nav.zhihu, href: routes.zhihu, color: '#1772f6', icon: undefined },
  { label: siteText.nav.mail, href: routes.mail, color: '#fe2222', icon: Mail },
]
</script>

<template>
  <footer class="px-20 pr-8 py-6 pt-0 flex justify-end gap-24 items-center">
    <!-- <a :href="withBase(routes.home)" class="text-white! text-xl font-[Georgia] italic mr-auto">Capybara &amp;
      Friends</a> -->
    <div class="flex gap-0">
      <a v-for="link in extraLinks"
        class="flex gap-2 items-center px-4 py-2 rounded-full group text-neutral-800! hover:text-(--color)!
        bg-transparent border border-transparent transition duration-250 hover:bg-white hover:border-neutral-300 hover:shadow-2xl/5 hover:-translate-y-0.5"
        :href="link.href" target="_blank" :style="{ '--color': link.color }">
        <component :is="link.icon ?? ArrowUpRight" :size="17" :stroke-width="1.8" class="text-inherit" />
        <span class="">{{ link.label }}</span>
      </a>
    </div>
  </footer>
</template>
