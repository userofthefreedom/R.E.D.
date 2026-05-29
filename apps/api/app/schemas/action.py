from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ActionNormalizeRequest(BaseModel):
    action_type: str


class ActionCreate(BaseModel):
    action_type: str
    current_use: str | None = None
    desired_use: str | None = None
    site_area: float | None = None
    building_area: float | None = None
    total_floor_area: float | None = None
    floor_count_above: int | None = None
    floor_count_under: int | None = None
    parking_before: int | None = None
    parking_after: int | None = None
    site_conditions: dict[str, Any] | None = None
    construction_method: str | None = None
    business_purpose: str | None = None
    memo: str | None = None
    normalized_json: dict[str, Any] = Field(default_factory=dict)


class ActionRead(ActionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime
