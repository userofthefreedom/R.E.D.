<script setup lang="ts">
import { LocateFixed, MapPin, Minus, Plus } from "@lucide/vue";
import { layerToggles } from "../../app/mockData";
</script>

<template>
  <div class="map-stack">
    <div class="map-mock" aria-label="선택 필지 지도 모형">
      <div class="map-tools">
        <button class="tool-square" title="확대"><Plus /></button>
        <button class="tool-square" title="축소"><Minus /></button>
        <button class="tool-square" title="현재 위치"><LocateFixed /></button>
      </div>

      <div class="road-line primary" />
      <div class="road-line secondary" />
      <div class="district-band" />
      <div class="parcel-neighbor one" />
      <div class="parcel-neighbor two" />
      <div class="parcel-shape" />
      <div class="map-pin"><MapPin /></div>
    </div>

    <div class="map-legend">
      <span class="map-legend-title">표시 레이어</span>
      <span v-for="layer in layerToggles" :key="layer.name" class="map-chip" :class="{ muted: !layer.enabled }">
        {{ layer.name }}
      </span>
      <span class="map-chip selected">선택 필지 · PNU 41287-10123-0123456</span>
    </div>
  </div>
</template>
