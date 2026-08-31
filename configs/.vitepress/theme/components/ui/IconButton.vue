<script setup lang="ts">
import type { Component } from 'vue'

withDefaults(defineProps<{
  icon: Component
  label: string
  href?: string
  active?: boolean
}>(), {
  active: false
})
</script>

<template>
  <a v-if="href" :href="href" class="icon-button" :class="{ 'is-active': active }" :aria-label="label" :title="label">
    <component :is="icon" :size="17" :stroke-width="1.8" aria-hidden="true" />
  </a>
  <button v-else type="button" class="icon-button" :class="{ 'is-active': active }" :aria-label="label" :title="label">
    <component :is="icon" :size="17" :stroke-width="1.8" aria-hidden="true" />
  </button>
</template>
