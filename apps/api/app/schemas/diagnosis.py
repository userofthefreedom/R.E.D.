from pydantic import BaseModel


class DiagnosisRunCreate(BaseModel):
    project_id: str

