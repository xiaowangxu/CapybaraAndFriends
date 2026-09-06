<script setup lang="ts">
import { ArrowUpRight, GitBranch, Mail, Rss } from '@lucide/vue'
import { withBase } from 'vitepress'
import { routes, siteText } from '../../data/site'

const extraLinks = [
  { label: siteText.nav.github, href: routes.github, color: '#ffffff', icon: GitBranch },
  { label: siteText.nav.zhihu, href: routes.zhihu, color: '#1772f6', icon: undefined },
  { label: siteText.nav.mail, href: routes.mail, color: '#fe2222', icon: Mail },
]
</script>

<template>
  <footer class="bg-neutral-900 px-20 pr-8 py-6 flex justify-end gap-24 items-center">
    <!-- <a :href="withBase(routes.home)" class="text-white! text-xl font-[Georgia] italic mr-auto">Capybara &amp;
      Friends</a> -->
    <div class="flex gap-0">
      <a v-for="link in extraLinks"
        class="flex gap-2 items-center hover:bg-neutral-700 px-4 py-2 rounded-full group text-white! hover:text-(--color)! transition-colors"
        :href="link.href" target="_blank" :style="{ '--color': link.color }">
        <component :is="link.icon ?? ArrowUpRight" :size="17" :stroke-width="1.8" class="text-inherit" />
        <span class="">{{ link.label }}</span>
      </a>
    </div>
  </footer>
</template>
