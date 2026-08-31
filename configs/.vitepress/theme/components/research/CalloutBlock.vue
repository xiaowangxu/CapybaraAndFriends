<script setup lang="ts">
withDefaults(defineProps<{ title?: string; kind?: string }>(), { title: 'Note', kind: 'note' })
</script>

<template>
  <aside class="research-callout">
    <p class="research-callout__title">{{ title }}</p>
    <div class="research-callout__body"><slot /></div>
  </aside>
</template>
