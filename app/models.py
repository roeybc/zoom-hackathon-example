from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None
    address: str | None = None