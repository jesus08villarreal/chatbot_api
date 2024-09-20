from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: Optional[str]
    name: str
    description: str
    named_as: str
    company_id: str