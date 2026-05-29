from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ParcelCreate(BaseModel):
    pnu: str
    standard_address: str | None = None
    jibun_address: str | None = None
    legal_dong_code: str | None = None
    land_category: str | None = None
    site_area: float | None = None
    use_district: str | None = None
    district_unit_plan: bool = False
    geometry_geojson: dict[str, Any] | None = None
    data_base_date: date | None = None
    collected_at: datetime | None = None


class ParcelRead(ParcelCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
