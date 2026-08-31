<script setup lang="ts">
defineProps<{ title?: string }>()
</script>

<template>
  <section class="interactive-figure">
    <h3 v-if="title">{{ title }}</h3>
    <slot><div class="interactive-figure__empty">Interactive component slot</div></slot>
  </section>
</template>
