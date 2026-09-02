<script setup lang="ts">
import CardLinkLabel from './CardLinkLabel.vue'
import CardShell from './CardShell.vue'
import type { NormalizedCardItem } from './types'
import { isExternalHttpUrl, resolveCardUrl } from './url'

defineProps<{
  card: NormalizedCardItem
}>()
</script>

<template>
  <CardShell :card="card">
    <img
      class="absolute bottom-0 right-0 z-0 mask-radial-[50%_90%] mask-radial-from-80%"
      :class="`image-card__media--${card.imageFit}`" :src="resolveCardUrl(card.image)" :alt="card.alt"
      :style="{ objectPosition: card.imagePosition }">
    <div class="absolute inset-0 flex flex-col gap-3 px-7 py-10 pr-12">
        <h2 v-if="card.title" class="text-black text-2xl font-[550]">{{ card.title }}</h2>
        <p v-if="card.description" class="text-sm text-neutral-500">{{ card.description }}</p>
    </div>
  </CardShell>
</template>
