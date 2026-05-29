import os
from pathlib import Path
from typing import Any

import httpx

from app.config import settings


class VWorldClient:
    address_url = "https://api.vworld.kr/req/address"
    data_url = "https://api.vworld.kr/req/data"

    def __init__(self, api_key: str | None = None, timeout: float = 6.0) -> None:
        self.api_key = api_key or settings.vworld_api_key or self._read_key_from_root_env()
        self.timeout = timeout

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def resolve_point(self, *, lon: float, lat: float) -> list[dict[str, Any]]:
        if not self.api_key:
            return []

        address_results = self._reverse_geocode(lon=lon, lat=lat)
        parcel_feature = self._fetch_cadastral_feature(lon=lon, lat=lat)

        if parcel_feature:
            return [self._candidate_from_feature(parcel_feature, address_results, lon, lat)]

        if address_results:
            return [self._candidate_from_address(address_results, lon, lat)]

        return []

    def _reverse_geocode(self, *, lon: float, lat: float) -> list[dict[str, Any]]:
        payload = self._get_json(
            self.address_url,
            {
                "service": "address",
                "request": "getAddress",
                "version": "2.0",
                "crs": "epsg:4326",
                "point": f"{lon},{lat}",
                "format": "json",
                "type": "both",
                "zipcode": "true",
                "simple": "false",
                "key": self.api_key,
            },
        )
        response = payload.get("response", {}) if payload else {}
        if response.get("status") != "OK":
            return []
        result = response.get("result")
        return result if isinstance(result, list) else []

    def _fetch_cadastral_feature(self, *, lon: float, lat: float) -> dict[str, Any] | None:
        payload = self._get_json(
            self.data_url,
            {
                "service": "data",
                "request": "GetFeature",
                "version": "2.0",
                "format": "json",
                "size": "1",
                "page": "1",
                "data": "LP_PA_CBND_BUBUN",
                "geomFilter": f"POINT({lon} {lat})",
                "geometry": "true",
                "attribute": "true",
                "crs": "EPSG:4326",
                "key": self.api_key,
            },
        )
        response = payload.get("response", {}) if payload else {}
        if response.get("status") != "OK":
            return None

        features = (
            response.get("result", {})
            .get("featureCollection", {})
            .get("features", [])
        )
        return features[0] if features else None

    def _candidate_from_feature(
        self,
        feature: dict[str, Any],
        address_results: list[dict[str, Any]],
        lon: float,
        lat: float,
    ) -> dict[str, Any]:
        properties = feature.get("properties", {}) if isinstance(feature, dict) else {}
        pnu = str(properties.get("pnu") or "")
        parcel_address = self._address_text(address_results, "parcel") or str(properties.get("addr") or "")
        road_address = self._address_text(address_results, "road") or parcel_address

        return {
            "pnu": pnu or f"VWORLD-{int(abs(lat) * 10000)}-{int(abs(lon) * 10000)}",
            "standard_address": road_address or parcel_address or f"VWorld 선택 위치 {lat:.5f}, {lon:.5f}",
            "jibun_address": parcel_address or str(properties.get("jibun") or ""),
            "legal_dong_code": pnu[:10] if len(pnu) >= 10 else "1168051000",
            "land_category": self._infer_land_category(properties),
            "site_area": self._number_or_default(properties.get("parea") or properties.get("shape_area"), 540.0),
            "use_district": "공공데이터 조회 필요",
            "district_unit_plan": False,
            "match_score": 98,
            "data_base_date": "2025-05-20",
            "public_data_status": "VWorld 지적도 조회",
            "centroid_lon": lon,
            "centroid_lat": lat,
            "geometry_geojson": feature.get("geometry"),
            "source_name": "VWorld Data API LP_PA_CBND_BUBUN",
        }

    def _candidate_from_address(
        self,
        address_results: list[dict[str, Any]],
        lon: float,
        lat: float,
    ) -> dict[str, Any]:
        parcel_address = self._address_text(address_results, "parcel")
        road_address = self._address_text(address_results, "road") or parcel_address
        legal_dong_code = self._legal_dong_code(address_results) or "1168051000"

        return {
            "pnu": f"{legal_dong_code}-{int(abs(lat) * 1000):05d}-{int(abs(lon) * 1000):07d}",
            "standard_address": road_address or f"VWorld 선택 위치 {lat:.5f}, {lon:.5f}",
            "jibun_address": parcel_address or "",
            "legal_dong_code": legal_dong_code,
            "land_category": "대",
            "site_area": 540.0,
            "use_district": "공공데이터 조회 필요",
            "district_unit_plan": False,
            "match_score": 88,
            "data_base_date": "2025-05-20",
            "public_data_status": "VWorld 역지오코딩",
            "centroid_lon": lon,
            "centroid_lat": lat,
            "geometry_geojson": None,
            "source_name": "VWorld Address API",
        }

    def _get_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        try:
            response = httpx.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
            return payload if isinstance(payload, dict) else {}
        except (httpx.HTTPError, ValueError):
            return {}

    def _address_text(self, address_results: list[dict[str, Any]], address_type: str) -> str | None:
        for item in address_results:
            if item.get("type") == address_type and item.get("text"):
                return str(item["text"])
        return None

    def _legal_dong_code(self, address_results: list[dict[str, Any]]) -> str | None:
        for item in address_results:
            structure = item.get("structure", {})
            code = structure.get("level4LC") if isinstance(structure, dict) else None
            if code:
                return str(code)
        return None

    def _infer_land_category(self, properties: dict[str, Any]) -> str:
        jibun = str(properties.get("jibun") or properties.get("addr") or "")
        return "도로" if "도" in jibun[-2:] else "대"

    def _number_or_default(self, value: Any, default: float) -> float:
        try:
            return round(float(value), 2)
        except (TypeError, ValueError):
            return default

    def _read_key_from_root_env(self) -> str | None:
        for path in self._candidate_env_paths():
            if not path.exists():
                continue
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.startswith("VWORLD_API_KEY="):
                    return line.split("=", 1)[1].strip() or None
        return os.getenv("VWORLD_API_KEY")

    def _candidate_env_paths(self) -> list[Path]:
        current = Path(__file__).resolve()
        return [
            Path.cwd() / ".env",
            current.parents[4] / ".env",
            current.parents[3] / ".env",
        ]
