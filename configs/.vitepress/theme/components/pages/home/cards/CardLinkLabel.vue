<script setup lang="ts">
import { ArrowRight } from '@lucide/vue'

defineProps<{
  label: string
}>()
</script>

<template>
  <span class="card-link-label">
    {{ label }}
    <ArrowRight :size="19" :stroke-width="1.5" aria-hidden="true" />
  </span>
</template>

<style scoped>
.card-link-label {
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  flex: 0 0 auto;
  font-size: .95rem;
  color: inherit;
  opacity: .76;
}

.card-link-label svg {
  transition: transform 180ms ease;
}
</style>
