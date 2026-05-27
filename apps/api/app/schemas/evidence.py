from pydantic import BaseModel


class EvidenceTraceRead(BaseModel):
    source_title: str

