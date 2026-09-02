<script setup lang="ts">
import { ref } from 'vue'
import CardLinkLabel from './CardLinkLabel.vue'
import CardShell from './CardShell.vue'
import TextCard from './TextCard.vue'
import type { NormalizedCardItem } from './types'
import { resolveCardUrl } from './url'

const props = defineProps<{
  card: NormalizedCardItem
}>()

</script>

<template>
  <CardShell :card="card">
    <img class="image-card__media" :class="`image-card__media--${card.imageFit}`" :src="resolveCardUrl(card.image)"
      :alt="card.alt" :style="{ objectPosition: card.imagePosition, background: card.config?.background }">
  </CardShell>
</template>

<style scoped>
.image-card__media {
  display: block;
  width: 100%;
  height: 100%;
  background: white;
}

.image-card__media--cover {
  object-fit: cover;
}

.image-card__media--contain {
  object-fit: contain;
}

.image-card__caption {
  position: absolute;
  inset-inline: .75rem;
  bottom: .75rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.15rem;
  border: 1px solid rgba(255, 255, 255, .14);
  border-radius: calc(var(--card-grid-radius) * .65);
  color: #fff;
  background: rgba(18, 18, 18, .72);
  backdrop-filter: blur(14px);
}

.image-card__copy {
  min-width: 0;
}

h2 {
  margin: 0;
  font-size: clamp(1.15rem, 1.7vw, 1.65rem);
  font-weight: 520;
  line-height: 1.2;
  letter-spacing: -.02em;
}

p {
  display: -webkit-box;
  margin: .4rem 0 0;
  overflow: hidden;
  color: rgba(255, 255, 255, .7);
  font-size: .85rem;
  line-height: 1.45;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

@media (max-width: 520px) {
  .image-card__caption {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
