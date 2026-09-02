<script setup lang="ts">
import { ref } from 'vue'
import CardLinkLabel from './CardLinkLabel.vue'
import CardShell from './CardShell.vue'
import TextCard from './TextCard.vue'
import type { NormalizedCardItem } from './types'
import { resolveCardUrl } from './url'

defineProps<{
  card: NormalizedCardItem
}>()

const imageFailed = ref(false)
</script>

<template>
  <TextCard v-if="imageFailed" :card="{ ...card, template: 'text' }" />
  <CardShell v-else :card="card">
    <div class="split-card" :class="`split-card--image-${card.imageSide}`">
      <div class="split-card__media">
        <img
          :src="resolveCardUrl(card.image)"
          :alt="card.alt"
          :style="{ objectFit: card.imageFit, objectPosition: card.imagePosition }"
          @error="imageFailed = true"
        >
      </div>
      <div class="split-card__content">
        <div>
          <h2 v-if="card.title">{{ card.title }}</h2>
          <p v-if="card.description">{{ card.description }}</p>
        </div>
        <CardLinkLabel v-if="card.url" :label="card.linkLabel || '探索'" />
      </div>
    </div>
  </CardShell>
</template>

<style scoped>
.split-card {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(0, .92fr);
  height: 100%;
}

.split-card--image-right .split-card__media {
  order: 2;
}

.split-card__media {
  min-width: 0;
  min-height: 0;
  overflow: hidden;
  background: #efeeeb;
}

.split-card__media img {
  display: block;
  width: 100%;
  height: 100%;
}

.split-card__content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 2rem;
  min-width: 0;
  padding: clamp(1.35rem, 2.7vw, 2.25rem);
}

h2 {
  margin: 0;
  font-size: clamp(1.45rem, 2vw, 2.3rem);
  font-weight: 480;
  line-height: 1.08;
  letter-spacing: -.035em;
}

p {
  margin: 1rem 0 0;
  color: #737373;
  font-size: .98rem;
  line-height: 1.65;
  white-space: pre-line;
}

:deep(.card-shell--dark) p {
  color: rgba(255, 255, 255, .65);
}

@media (max-width: 767px) {
  .split-card {
    grid-template-columns: 1fr;
    grid-template-rows: 13rem minmax(0, 1fr);
  }

  .split-card--image-right .split-card__media {
    order: initial;
  }
}
</style>
