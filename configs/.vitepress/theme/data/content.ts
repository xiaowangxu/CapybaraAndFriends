import { data as contentData } from '../../data/content.data'
import type { DocRecord } from '../../data/content.data'

export type { DocRecord }
export const docs = contentData as DocRecord[]

export function researchArticles() {
  return docs
    .filter(record => record.frontmatter.layout === 'article')
    .sort((a, b) => {
      const aDate = Date.parse(String(a.frontmatter.date || '')) || 0
      const bDate = Date.parse(String(b.frontmatter.date || '')) || 0
      return bDate - aDate
    })
}

export function findDoc(url: string) {
  const normalized = url.replace(/\/+$/, '') || '/'
  return docs.find(record => (record.url.replace(/\/+$/, '') || '/') === normalized)
}

export function displayValue(value: unknown, fallback = '') {
  return value === undefined || value === null || value === '' ? fallback : String(value)
}

export function formatDate(value: unknown) {
  const date = new Date(String(value || ''))
  if (Number.isNaN(date.getTime())) return displayValue(value, '—')
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC'
  }).format(date)
}
