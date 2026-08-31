<script setup lang="ts">
interface Option {
  label: string
  value: string
}

defineProps<{
  options: Option[]
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <div class="segmented-control" role="tablist">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      role="tab"
      class="segmented-control__button"
      :class="{ 'is-selected': option.value === modelValue }"
      :aria-selected="option.value === modelValue"
      @click="emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>
