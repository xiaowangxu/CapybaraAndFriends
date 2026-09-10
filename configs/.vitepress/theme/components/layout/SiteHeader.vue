<script setup lang="ts">
import { withBase } from 'vitepress'
import { routes, siteText } from '../../data/site'
import BrandMark from '../ui/BrandMark.vue'
import { ArrowUpRight, GitBranch, Mail, TextAlignJustify } from '@lucide/vue';
import { onBeforeUnmount, onMounted, ref, watch } from 'vue';

const links = [
  { label: siteText.nav.research, href: routes.research },
]

const extraLinks = [
  { label: siteText.nav.github, href: routes.github, color: '#1f2328', icon: GitBranch },
  { label: siteText.nav.zhihu, href: routes.zhihu, color: '#1772f6', icon: undefined },
  { label: siteText.nav.mail, href: routes.mail, color: '#fe2222', icon: Mail },
]

const expanded = ref(true)

const margin = 50
let lastScrollY: number | undefined = undefined
const scrollOutOfBound = ref(false)

function onScroll(evt?: Event) {
  let scrollDown = false
  const scrollY = window.scrollY
  if (lastScrollY !== undefined) {
    scrollDown = scrollY - lastScrollY > 0
  }
  lastScrollY = scrollY
  if (scrollDown) {
    if (scrollOutOfBound.value) clickOutside()
    scrollOutOfBound.value = scrollY > margin
  }
  if (scrollY <= margin) {
    scrollOutOfBound.value = false;
  }
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll)
})
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})

watch(scrollOutOfBound, v => {
  if (v) {
    expanded.value = false
  } else {
    expanded.value = true
  }
})

function clickOutside() {
  if (scrollOutOfBound.value) {
    expanded.value = false
  }
}

</script>

<template>
  <header class="px-10 pt-6 pb-4 fixed top-0 flex z-100 w-full overflow-hidden">
    <div class="transition-[width] duration-400 delay-100 ease-in-out" :class="[expanded ? 'w-[calc((100%-1400px)/2)]' : 'w-0']">
    </div>
    <div ref="dynamicIsland"
      class="bg-white outline outline-neutral-300 rounded-full shadow-lg/5 flex overflow-hidden transition-[width] duration-350 ease-in-out"
      :class="[expanded ? 'w-[1400px]' : 'w-[106px]']">
      <a :href="withBase(routes.home)"
        class="inline-flex min-h-14 max-h-14 h-14 w-12 min-w-12.5 justify-end items-center mr-2"
        aria-label="Capybara & Friends">
        <BrandMark />
      </a>
      <Transition name="slide-fade" mode="out-in">
        <nav v-if="!expanded" class="flex items-center min-h-14 max-h-14 h-14 p-2 pl-0">
          <a
            class="rounded-full h-full aspect-square text-sm flex justify-center items-center text-neutral-400! hover:text-black! hover:bg-neutral-100 transition-colors text-nowrap"
            @click="expanded = true">
            <TextAlignJustify :size="20" :stroke-width="1.8" class="text-inherit" />
          </a>
        </nav>
        <nav v-else class="flex-1 flex items-center min-h-14 max-h-14 h-14 p-2 pl-0 w-7xl max-w-full overflow-hidden">
          <a v-for="link in links" :key="link.href" :href="withBase(link.href)"
            class="rounded-full px-3 h-full text-sm flex justify-center items-center text-neutral-800! hover:text-black! hover:bg-neutral-100 transition-colors text-nowrap">{{
              link.label }}</a>
          <div class="flex-1" />
          <a v-for="link in extraLinks" class="flex gap-2 px-3 py-2 group text-neutral-800! hover:text-(--color)!
        rounded-full h-full text-sm justify-center items-center hover:bg-neutral-100 transition-colors text-nowrap"
            :href="link.href" target="_blank" :style="{ '--color': link.color }">
            <component :is="link.icon ?? ArrowUpRight" :size="17" :stroke-width="1.8" class="text-inherit" />
            <span class="">{{ link.label }}</span>
          </a>
        </nav>
      </Transition>
    </div>
    <!-- <div class="flex-1 bg-amber-300 transition-all duration-400"></div> -->
  </header>
</template>

<style scoped>
/* 滑动淡出动画 */
.slide-fade-enter-active {
  transition: all 250ms cubic-bezier(0, 0, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 250ms cubic-bezier(0.4, 0, 1, 1);
}

/* 进入动画：从下方滑入并淡入 */
.slide-fade-enter-from {
  transform: translateY(100%);
  opacity: 0;
  filter: blur(6px);
}

.slide-fade-enter-to {
  transform: translateY(0);
  opacity: 1;
  filter: blur(0px);
}

/* 离开动画：向上滑出并淡出 */
.slide-fade-leave-from {
  transform: translateY(0);
  opacity: 1;
  filter: blur(0px);
}

.slide-fade-leave-to {
  transform: translateY(-100%);
  opacity: 0;
  filter: blur(6px);
}
</style>