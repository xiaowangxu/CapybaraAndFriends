<script setup lang="ts">
import { computed } from 'vue'
import type { NormalizedCardItem } from './types'
import { isExternalHttpUrl, resolveCardUrl } from './url'

const props = defineProps<{
  card: NormalizedCardItem
}>()

const href = computed(() => resolveCardUrl(props.card.url))
const isExternal = computed(() => Boolean(props.card.url && isExternalHttpUrl(props.card.url)))
const tag = computed(() => href.value ? 'a' : 'article')
</script>

<template>
  <component :is="tag"
    class="contain-paint block w-full h-full relative rounded-2xl overflow-hidden border border-neutral-300 hover:shadow-2xl/5 hover:-translate-y-0.5 transition duration-250"
    :class="[card.tone === 'light' ? 'bg-white' : 'bg-neutral-700']" :style="{ background: card.background }" :href="href"
    :target="isExternal ? '_blank' : undefined" :rel="isExternal ? 'noopener noreferrer' : undefined"
    :aria-label="href ? card.title : undefined">
    <slot />
  </component>
</template>
