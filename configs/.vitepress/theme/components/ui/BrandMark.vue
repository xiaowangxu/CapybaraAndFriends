<script setup lang="ts">
import { withBase } from 'vitepress'
</script>

<template>
  <span class="w-9 aspect-square">
    <img :src="withBase('/assets/capybara.png')" alt="" aria-hidden="true" />
  </span>
</template>
