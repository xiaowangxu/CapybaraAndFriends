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
    <shader-doodle v-if="card.config?.shader" shadertoy class="absolute inset-0 z-0 w-full h-full">
      <component is="script" type="x-shader/x-fragment">
        {{ card.config?.shader }}
      </component>
    </shader-doodle>
    <div class="absolute inset-0 flex flex-col gap-3 px-9 py-9">
      <h2 v-if="card.title" class="text-2xl font-[550]" :class="[card.tone === 'light' ? 'text-black' : 'text-white']">
        {{ card.title }}</h2>
      <p v-if="card.description" class="text-sm"
        :class="[card.tone === 'light' ? 'text-black/60' : 'text-white/60']">{{ card.description }}</p>
    </div>
  </CardShell>
</template>
