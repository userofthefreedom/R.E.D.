from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class BuildingCreate(BaseModel):
    parcel_id: str | None = None
    registry_pk: str | None = None
    name: str | None = None
    main_use: str | None = None
    building_area: float | None = None
    total_floor_area: float | None = None
    floor_count_above: int | None = None
    floor_count_under: int | None = None
    approval_date: date | None = None
    raw_payload: dict[str, Any] | None = None


class BuildingRead(BuildingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
