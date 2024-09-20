from pydantic import BaseModel, Field
from typing import Optional

class Company(BaseModel):
    id: Optional[str]
    name: str
    description: str