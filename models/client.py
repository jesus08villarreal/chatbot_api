from pydantic import BaseModel, Field
from typing import Optional

class Client(BaseModel):
    id: Optional[str]
    name: str
    description: str
    named_as: str
    address: str
    email: str
    phone: str
    company_id: str    

