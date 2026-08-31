<script setup lang="ts">
import { computed } from 'vue'
import { ArrowUpRight, CircleDot, FileText } from '@lucide/vue'
import { useData } from 'vitepress'

const { frontmatter } = useData()
const projects = computed(() => Array.isArray(frontmatter.value.projects) ? frontmatter.value.projects : [])
</script>

<template>
  <main class="content-page page-container">
    <header class="page-intro">
      <p class="section-label"><FileText :size="15" :stroke-width="1.8" />{{ frontmatter.sectionLabel || 'Capybara & Friends' }}</p>
      <h1>{{ frontmatter.title }}</h1>
      <p v-if="frontmatter.description">{{ frontmatter.description }}</p>
    </header>

    <section v-if="projects.length" class="project-grid project-grid--content">
      <a v-for="(project, index) in projects" :key="project.name" href="#project-details" class="project-tile">
        <div class="project-tile__top"><span>0{{ index + 1 }}</span><ArrowUpRight :size="16" :stroke-width="1.8" /></div>
        <h2>{{ project.name }}</h2>
        <p>{{ project.description }}</p>
        <span class="project-tile__status"><CircleDot :size="13" :stroke-width="1.8" />{{ project.status }}</span>
      </a>
    </section>

    <article id="project-details" class="article-content content-page__body"><slot /></article>
  </main>
</template>
