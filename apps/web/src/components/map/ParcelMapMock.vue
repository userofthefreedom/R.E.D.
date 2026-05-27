<script setup lang="ts">
import { LocateFixed, MapPin, Minus, Plus } from "@lucide/vue";
</script>

<template>
  <div class="map-mock" aria-label="선택 필지 지도 모형">
    <div class="map-tools">
      <button class="tool-square" title="확대"><Plus /></button>
      <button class="tool-square" title="축소"><Minus /></button>
      <button class="tool-square" title="현재 위치"><LocateFixed /></button>
    </div>
    <div class="parcel-shape" />
    <div class="map-pin"><MapPin /></div>
  </div>
</template>
