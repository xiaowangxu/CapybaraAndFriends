import { defineConfig } from 'vitepress'
import tailwindcss from '@tailwindcss/vite'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: '/CapybaraAndFriends/',
  srcDir: '../docs',
  title: 'Capybara & Friends',
  description: 'sunwx的乱七八糟',
  head: [['link', { rel: 'icon', href: '/CapybaraAndFriends/assets/capybara.png' }]],
  lang: 'zh-CN',
  cleanUrls: true,
  appearance: false,
  markdown: {
    math: true
  },
  vite: {
    plugins: [tailwindcss()]
  },
  vue: {
    template: {
      compilerOptions: {
        // Treat shader-doodle as a native custom element
        isCustomElement: (tag) => tag === 'shader-doodle'
      }
    }
  }
})
