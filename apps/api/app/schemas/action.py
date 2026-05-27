from pydantic import BaseModel


class ActionNormalizeRequest(BaseModel):
    action_type: str

