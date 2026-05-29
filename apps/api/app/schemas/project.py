from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    address: str | None = None
    pnu: str | None = None
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    risk_level: str | None = None
    address: str | None = None
    pnu: str | None = None
    description: str | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str | None = None
    name: str
    status: str
    risk_level: str | None = None
    address: str | None = None
    pnu: str | None = None
    description: str | None = None
    created_at: datetime
    updated_at: datetime
