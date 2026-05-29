<script setup lang="ts">
import { LocateFixed, MapPin, Minus, Plus } from "@lucide/vue";
import "ol/ol.css";
import Feature from "ol/Feature";
import GeoJSON from "ol/format/GeoJSON";
import Map from "ol/Map";
import View from "ol/View";
import Point from "ol/geom/Point";
import Polygon from "ol/geom/Polygon";
import type { Geometry } from "ol/geom";
import VectorLayer from "ol/layer/Vector";
import { fromLonLat, toLonLat } from "ol/proj";
import VectorSource from "ol/source/Vector";
import { Fill, Icon, Stroke, Style } from "ol/style";
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import { layerToggles } from "../../app/mockData";
import { createBaseMapLayer, getMapProviderConfig } from "./mapProvider";

const mapElement = ref<HTMLDivElement | null>(null);
let map: Map | null = null;
let parcelFeature: Feature<Geometry> | null = null;
let pinFeature: Feature<Point> | null = null;
const mapProviderLabel = getMapProviderConfig().label;
const props = defineProps<{
  selectedLon?: number | null;
  selectedLat?: number | null;
  selectedGeometry?: Record<string, unknown> | null;
  selectedPnu?: string | null;
}>();
const emit = defineEmits<{
  select: [{ lon: number; lat: number }];
}>();

const defaultLonLat: [number, number] = [127.0365, 37.5007];
let selectedCenter = fromLonLat(defaultLonLat);

function createParcelPolygon(lon: number, lat: number) {
  return new Polygon([[
    fromLonLat([lon - 0.00135, lat + 0.00075]),
    fromLonLat([lon + 0.00100, lat + 0.00105]),
    fromLonLat([lon + 0.00145, lat - 0.00080]),
    fromLonLat([lon - 0.00105, lat - 0.00110]),
    fromLonLat([lon - 0.00135, lat + 0.00075]),
  ]]);
}

function readSelectedGeometry(lon: number, lat: number) {
  if (props.selectedGeometry) {
    try {
      return new GeoJSON().readGeometry(props.selectedGeometry, {
        dataProjection: "EPSG:4326",
        featureProjection: "EPSG:3857",
      });
    } catch {
      return createParcelPolygon(lon, lat);
    }
  }
  return createParcelPolygon(lon, lat);
}

function updateSelectedFeature(lon: number, lat: number, shouldAnimate = true) {
  selectedCenter = fromLonLat([lon, lat]);
  parcelFeature?.setGeometry(readSelectedGeometry(lon, lat));
  pinFeature?.setGeometry(new Point(selectedCenter));
  if (shouldAnimate) {
    map?.getView().animate({ center: selectedCenter, duration: 180 });
  }
}

onMounted(() => {
  if (!mapElement.value) return;
  const initialLon = props.selectedLon ?? defaultLonLat[0];
  const initialLat = props.selectedLat ?? defaultLonLat[1];
  selectedCenter = fromLonLat([initialLon, initialLat]);

  parcelFeature = new Feature(readSelectedGeometry(initialLon, initialLat));
  parcelFeature.setStyle(new Style({
    fill: new Fill({ color: "rgba(63, 111, 159, 0.30)" }),
    stroke: new Stroke({ color: "#2f5f91", width: 4 }),
  }));

  pinFeature = new Feature(new Point(selectedCenter));
  pinFeature.setStyle(new Style({
    image: new Icon({
      src: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='42' height='42' viewBox='0 0 24 24' fill='%233f6f9f' stroke='white' stroke-width='1.6'><path d='M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0'/><circle cx='12' cy='10' r='3' fill='white' stroke='%233f6f9f'/></svg>",
      anchor: [0.5, 1],
      scale: 1,
    }),
  }));

  map = new Map({
    target: mapElement.value,
    layers: [
      createBaseMapLayer(),
      new VectorLayer({ source: new VectorSource({ features: [parcelFeature, pinFeature] }) }),
    ],
    view: new View({ center: selectedCenter, zoom: 16.5 }),
    controls: [],
  });

  map.on("singleclick", (event) => {
    const [lon, lat] = toLonLat(event.coordinate);
    updateSelectedFeature(lon, lat);
    emit("select", { lon, lat });
  });
});

watch(
  () => [props.selectedLon, props.selectedLat, props.selectedGeometry] as const,
  ([lon, lat]) => {
    if (typeof lon === "number" && typeof lat === "number") {
      updateSelectedFeature(lon, lat);
    }
  },
);

onBeforeUnmount(() => {
  map?.setTarget(undefined);
  map = null;
});

function zoomBy(delta: number) {
  const view = map?.getView();
  const zoom = view?.getZoom();
  if (view && zoom !== undefined) {
    view.animate({ zoom: zoom + delta, duration: 160 });
  }
}

function recenter() {
  map?.getView().animate({ center: selectedCenter, duration: 180 });
}
</script>

<template>
  <div class="map-stack">
    <div class="map-mock actual-map" aria-label="선택 필지 실제 지도">
      <div ref="mapElement" class="map-canvas" />
      <div class="map-tools">
        <button class="tool-square" title="확대" @click="zoomBy(1)"><Plus /></button>
        <button class="tool-square" title="축소" @click="zoomBy(-1)"><Minus /></button>
        <button class="tool-square" title="선택 필지로 이동" @click="recenter"><LocateFixed /></button>
      </div>
      <div class="map-watermark"><MapPin /> {{ mapProviderLabel }} 지도 타일 · 클릭 위치 선택</div>
    </div>

    <div class="map-legend">
      <span class="map-legend-title">표시 레이어</span>
      <span v-for="layer in layerToggles" :key="layer.name" class="map-chip" :class="{ muted: !layer.enabled }">
        {{ layer.name }}
      </span>
      <span class="map-chip selected">선택 필지 · PNU {{ props.selectedPnu ?? "지도 클릭 대기" }}</span>
    </div>
  </div>
</template>
