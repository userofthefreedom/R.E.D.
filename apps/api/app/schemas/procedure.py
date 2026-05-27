from pydantic import BaseModel


class ProcedureResultRead(BaseModel):
    procedure_type: str
    target: bool

