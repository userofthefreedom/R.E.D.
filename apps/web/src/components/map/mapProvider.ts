import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import XYZ from "ol/source/XYZ";

type MapProvider = "osm" | "custom";

interface MapProviderConfig {
  label: string;
  provider: MapProvider;
  urlTemplate?: string;
}

export function getMapProviderConfig(): MapProviderConfig {
  const urlTemplate = import.meta.env.VITE_MAP_TILE_URL_TEMPLATE as string | undefined;

  if (urlTemplate) {
    return {
      label: import.meta.env.VITE_MAP_TILE_LABEL ?? "공식 지도 API",
      provider: "custom",
      urlTemplate,
    };
  }

  return {
    label: "OpenStreetMap",
    provider: "osm",
  };
}

export function createBaseMapLayer() {
  const config = getMapProviderConfig();

  if (config.provider === "custom" && config.urlTemplate) {
    return new TileLayer({
      source: new XYZ({
        url: config.urlTemplate,
        crossOrigin: "anonymous",
      }),
    });
  }

  return new TileLayer({ source: new OSM() });
}
