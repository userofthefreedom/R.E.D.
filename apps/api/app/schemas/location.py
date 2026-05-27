from pydantic import BaseModel


class LocationResolveRequest(BaseModel):
    query: str

