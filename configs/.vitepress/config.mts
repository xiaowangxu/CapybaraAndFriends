import { defineConfig } from 'vitepress'
import tailwindcss from '@tailwindcss/vite'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: '/CapybaraAndFriends/',
  srcDir: '../docs',
  title: 'Capybara & Friends',
  description: 'sunwx的乱七八糟',
  lang: 'zh-CN',
  cleanUrls: true,
  appearance: false,
  markdown: {
    math: true
  },
  vite: {
    plugins: [tailwindcss()]
  }
})
