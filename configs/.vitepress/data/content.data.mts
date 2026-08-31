import { createContentLoader, type ContentData } from 'vitepress'

export interface DocRecord {
  url: string
  slug: string
  section: string
  frontmatter: Record<string, any>
  excerpt?: string
}

function normalizeRecord(item: ContentData): DocRecord {
  const cleanUrl = item.url.replace(/\/+$/, '') || '/'
  const segments = cleanUrl.split('/').filter(Boolean)

  return {
    url: item.url,
    slug: segments[segments.length - 1] || 'home',
    section: segments[0] || 'home',
    frontmatter: item.frontmatter,
    excerpt: item.excerpt
  }
}

export default createContentLoader('**/*.md', {
  excerpt: true,
  transform(data) {
    return data
      .map(normalizeRecord)
      .filter(record => record.frontmatter.hidden !== true)
  }
})
