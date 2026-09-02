import type { Component } from 'vue'
import ImageCard from './ImageCard.vue'
import SplitCard from './SplitCard.vue'
import TextCard from './TextCard.vue'
import type { CardTemplateName } from './types'

export const cardTemplates: Record<CardTemplateName, Component> = {
  image: ImageCard,
  text: TextCard,
  split: SplitCard
}

export const isCardTemplateName = (value: string): value is CardTemplateName => value in cardTemplates

export type { CardGridConfig, CardItem, CardTemplateName, NormalizedCardItem } from './types'
