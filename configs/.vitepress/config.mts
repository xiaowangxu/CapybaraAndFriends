import { defineConfig } from 'vitepress'
import tailwindcss from '@tailwindcss/vite'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: '../docs',
  title: 'Capybara & Friends',
  description: '独立研究机构',
  lang: 'zh-CN',
  cleanUrls: true,
  appearance: false,
  vite: {
    plugins: [tailwindcss()]
  }
})
