<script setup lang="ts">
import { withBase } from 'vitepress';
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
    <div v-if="card.image" class="absolute inset-0 z-0 bg-cover bg-no-repeat bg-center" :style="{ backgroundImage: `url(${withBase(card.image)})` }" />
    <div class="absolute inset-0 flex flex-col gap-3 px-8 py-9 pr-12">
      <h2 v-if="card.title" class="text-black text-2xl font-[550]">{{ card.title }}</h2>
      <p v-if="card.description" class="text-sm text-neutral-500">{{ card.description }}</p>
    </div>
  </CardShell>
</template>
