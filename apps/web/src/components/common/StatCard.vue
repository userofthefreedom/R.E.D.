<script setup lang="ts">
import type { Component } from "vue";

defineProps<{
  label: string;
  value: string | number;
  hint?: string;
  icon: Component;
  tone?: "green" | "blue" | "violet" | "amber";
}>();
</script>

<template>
  <article class="card metric">
    <div>
      <span class="subtle">{{ label }}</span>
      <strong>{{ value }}</strong>
      <span v-if="hint" class="subtle">{{ hint }}</span>
    </div>
    <span class="metric-icon" :class="tone">
      <component :is="icon" />
    </span>
  </article>
</template>
