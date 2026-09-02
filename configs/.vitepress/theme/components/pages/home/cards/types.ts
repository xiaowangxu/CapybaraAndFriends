export type CardTemplateName = 'image' | 'text' | 'split' | 'pure-image'
export type CardImageFit = 'cover' | 'contain'
export type CardImagePosition = 'center' | 'top' | 'right' | 'bottom' | 'left'
export type CardImageSide = 'left' | 'right'
export type CardTone = 'dark' | 'light'

export interface CardItem {
  id?: string
  template?: CardTemplateName | string
  title?: string
  description?: string
  image?: string
  alt?: string
  url?: string
  linkLabel?: string
  colSpan?: number
  rowSpan?: number
  imageFit?: CardImageFit
  imagePosition?: CardImagePosition
  imageSide?: CardImageSide
  tone?: CardTone
  config?: Record<string, any> | Array<any>
}

export interface CardGridConfig {
  columns?: number
  rowHeight?: number
  cards?: CardItem[]
}

export interface NormalizedCardItem extends CardItem {
  id: string
  template: CardTemplateName
  title: string
  description: string
  colSpan: number
  rowSpan: number
  tabletColSpan: number
  imageFit: CardImageFit
  imagePosition: CardImagePosition
  imageSide: CardImageSide
}
