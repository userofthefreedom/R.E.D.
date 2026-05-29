from typing import Any

from pydantic import BaseModel, Field


class LocationResolveRequest(BaseModel):
    query: str = Field(default="", description="Address, jibun, PNU, or coordinate text")
    mode: str = "address"
    lon: float | None = None
    lat: float | None = None


class LocationCandidate(BaseModel):
    pnu: str
    standard_address: str
    jibun_address: str
    legal_dong_code: str
    land_category: str
    site_area: float
    use_district: str
    district_unit_plan: bool
    match_score: int
    data_base_date: str
    public_data_status: str
    centroid_lon: float | None = None
    centroid_lat: float | None = None
    geometry_geojson: dict[str, Any] | None = None
    source_name: str | None = None


class LocationResolveResponse(BaseModel):
    query: str
    mode: str
    status: str
    provider: str
    candidates: list[LocationCandidate]
