from pydantic import BaseModel

class RequestModel(BaseModel):
    id: int
    user_id: int
    username: str | None
    comment: str
    status: str

    class Config:
        from_attributes = True