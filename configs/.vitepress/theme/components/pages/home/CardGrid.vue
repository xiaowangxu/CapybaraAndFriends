<script setup lang="ts">
import { computed, type CSSProperties } from 'vue'
import { cardTemplates, isCardTemplateName } from './cards'
import type {
  CardGridConfig,
  CardItem,
  CardTemplateName,
  NormalizedCardItem
} from './cards/types'

const props = defineProps<{
  config: CardGridConfig
}>()

const clampNumber = (value: unknown, fallback: number, min: number, max: number) => {
  const number = Number(value)
  return Number.isFinite(number) ? Math.min(max, Math.max(min, Math.round(number))) : fallback
}

const warn = (message: string) => {
  if (import.meta.env.DEV) console.warn(`[CardGrid] ${message}`)
}

const normalizedConfig = computed(() => {
  const columns = clampNumber(props.config?.columns, 6, 1, 12)
  const rawCards = Array.isArray(props.config?.cards) ? props.config.cards : []

  const cards = rawCards.flatMap((rawCard, index) => {
    if (!rawCard || typeof rawCard !== 'object') {
      warn(`第 ${index + 1} 张卡片不是有效对象，已忽略。`)
      return []
    }

    const card = rawCard as CardItem
    const requestedTemplate = String(card.template || 'text')
    let template: CardTemplateName = isCardTemplateName(requestedTemplate) ? requestedTemplate : 'text'

    if (!isCardTemplateName(requestedTemplate)) {
      warn(`未知模板 “${requestedTemplate}”，已回退为 text。`)
    }

    if ((template === 'image' || template === 'split') && !card.image) {
      warn(`“${card.title || `第 ${index + 1} 张卡片`}” 缺少图片，已回退为 text。`)
      template = 'text'
    }

    const title = String(card.title || '').trim()
    const description = String(card.description || '').trim()
    if (!title && !description) {
      warn(`第 ${index + 1} 张卡片没有标题或描述，已忽略。`)
      return []
    }

    const colSpan = clampNumber(card.colSpan, 1, 1, columns)
    const rowSpan = clampNumber(card.rowSpan, 1, 1, 6)
    const tabletColSpan = Math.min(3, Math.max(1, Math.ceil((colSpan / columns) * 3)))

    return [{
      ...card,
      id: String(card.id || card.url || `${template}-${index}`),
      template,
      title,
      description,
      image: card.image ? String(card.image) : undefined,
      alt: String(card.alt || title),
      url: card.url ? String(card.url) : undefined,
      linkLabel: card.linkLabel ? String(card.linkLabel) : undefined,
      colSpan,
      rowSpan,
      tabletColSpan,
      imageFit: card.imageFit === 'contain' ? 'contain' : 'cover',
      imagePosition: ['center', 'top', 'right', 'bottom', 'left'].includes(String(card.imagePosition))
        ? card.imagePosition!
        : 'center',
      imageSide: card.imageSide === 'right' ? 'right' : 'left',
      config: card.config
    } satisfies NormalizedCardItem]
  })

  return {
    columns,
    rowHeight: clampNumber(props.config?.rowHeight, 180, 96, 360),
    cards
  }
})

const gridStyle = computed(() => ({
  '--card-grid-columns': normalizedConfig.value.columns,
  '--card-grid-row-height': `${normalizedConfig.value.rowHeight}px`,
}) as CSSProperties)

const cardStyle = (card: NormalizedCardItem) => ({
  '--card-col-span': card.colSpan,
  '--card-row-span': card.rowSpan,
  '--card-tablet-col-span': card.tabletColSpan
}) as CSSProperties
</script>

<template>
  <section
    v-if="normalizedConfig.cards.length"
    class="card-grid-section"
    aria-label="精选内容"
  >
    <div class="card-grid" :style="gridStyle">
      <div
        v-for="card in normalizedConfig.cards"
        :key="card.id"
        class="card-grid__item"
        :class="`card-grid__item--${card.template}`"
        :style="cardStyle(card)"
      >
        <component :is="cardTemplates[card.template]" :card="card" />
      </div>
    </div>
  </section>
</template>

<style scoped>
@reference '../../../style.css';

.card-grid {
  @apply gap-3;
  display: grid;
  grid-template-columns: repeat(var(--card-grid-columns), minmax(0, 1fr));
  grid-auto-rows: var(--card-grid-row-height);
  grid-auto-flow: dense;
}

.card-grid__item {
  min-width: 0;
  min-height: 0;
  grid-column: span var(--card-col-span);
  grid-row: span var(--card-row-span);
}
</style>
