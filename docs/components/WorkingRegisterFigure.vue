<script setup lang="ts">
import { withBase } from 'vitepress'

defineProps<{ name: string; alt: string }>()
</script>

<template>
  <figure class="working-register-figure">
    <div class="wr-figure-toolbar">
      <span>小屏可横向滑动查看</span>
      <a :href="withBase(`/assets/working-registers/${name}.svg`)" target="_blank" rel="noopener"
        :aria-label="`查看原图：${alt}`">查看 SVG 原图 ↗</a>
    </div>
    <div class="wr-figure-scroll" tabindex="0" role="region" :aria-label="alt">
      <img :src="withBase(`/assets/working-registers/${name}.svg`)" :alt="alt" loading="lazy">
    </div>
  </figure>
</template>

<style scoped>
.working-register-figure { max-width: 1100px !important; margin: 2.5rem auto; }
.wr-figure-toolbar { display: flex; justify-content: space-between; gap: 1rem; font-size: .8rem; margin-bottom: .6rem; }
.wr-figure-toolbar span { color: #65736e; }
.wr-figure-scroll { max-width: 100%; overflow-x: auto; border: 1px solid #dde5df; border-radius: 12px; background: white; }
.wr-figure-scroll:focus-visible { outline: 2px solid #267c6d; outline-offset: 3px; }
.wr-figure-scroll img { width: 100%; min-width: 850px; max-width: none; height: auto; margin: 0; }
@media (min-width: 900px) { .wr-figure-toolbar span { visibility: hidden; } }
@media print { .wr-figure-toolbar { display: none; } .wr-figure-scroll img { min-width: 0; } }
</style>

<style>
/* Scope mobile adjustments to this article; other article layouts keep their styles. */
@media (max-width: 600px) {
  .article-page:has(.working-register-figure) > header h1 {
    font-size: 2rem;
    line-height: 1.4;
    overflow-wrap: anywhere;
    text-wrap: balance;
  }
  .article-page:has(.working-register-figure) > header { padding-bottom: 3rem; }
  .article-page:has(.working-register-figure) > div:has(> .article-content) { padding-inline: 20px; }
  .article-page:has(.working-register-figure) .article-content { overflow-wrap: anywhere; }
}
</style>
