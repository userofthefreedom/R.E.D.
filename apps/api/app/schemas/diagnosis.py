from datetime import datetime

from pydantic import ConfigDict
from pydantic import BaseModel


class DiagnosisRunCreate(BaseModel):
    project_id: str
    action_id: str | None = None
    rule_set_version: str | None = "rule-set-v0.1.0"
    rag_index_version: str | None = "legal-index-v0.1.0"
    data_base_date: str | None = "2025-05-20"
    law_base_date: str | None = "2025-05-20"


class DiagnosisRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    action_id: str | None = None
    status: str
    rule_set_version: str | None = None
    rag_index_version: str | None = None
    data_base_date: str | None = None
    law_base_date: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class DiagnosisStatusRead(BaseModel):
    run_id: str
    status: str
    message: str
