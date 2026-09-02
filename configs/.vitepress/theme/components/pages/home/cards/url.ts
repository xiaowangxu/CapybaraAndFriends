import { withBase } from 'vitepress'

const SCHEME_PATTERN = /^[a-z][a-z\d+.-]*:/i

export const isExternalHttpUrl = (value: string) => /^https?:\/\//i.test(value) || value.startsWith('//')

export const resolveCardUrl = (value?: string) => {
  if (!value) return undefined
  if (SCHEME_PATTERN.test(value) || value.startsWith('//') || value.startsWith('#')) return value
  return withBase(value.startsWith('/') ? value : `/${value}`)
}
