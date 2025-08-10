from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    address: Optional[str] = None