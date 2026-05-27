from pydantic import BaseModel


class ReportCreate(BaseModel):
    diagnosis_run_id: str

