from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    phone: str
    name: str
    company_id: str