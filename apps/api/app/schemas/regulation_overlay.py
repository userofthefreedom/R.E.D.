from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class RegulationOverlayCreate(BaseModel):
    parcel_id: str | None = None
    layer_code: str | None = None
    layer_name: str
    regulation_type: str | None = None
    jurisdiction: str | None = None
    overlap_area: float | None = None
    overlap_ratio: float | None = None
    source_name: str | None = None
    source_url: str | None = None
    data_base_date: date | None = None
    collected_at: datetime | None = None
    raw_payload: dict[str, Any] | None = None


class RegulationOverlayRead(RegulationOverlayCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
