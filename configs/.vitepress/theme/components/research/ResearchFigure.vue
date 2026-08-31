<script setup lang="ts">
defineProps<{ title?: string; caption?: string; number?: string | number }>()
</script>

<template>
  <figure class="research-figure">
    <div class="research-figure__heading">
      <strong v-if="title">{{ title }}</strong>
      <span v-if="number" class="text-zinc-500">Figure {{ number }}</span>
    </div>
    <div class="research-figure__canvas"><slot /></div>
    <figcaption v-if="caption" class="research-figure__caption">{{ caption }}</figcaption>
  </figure>
</template>
