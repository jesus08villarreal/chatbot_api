from pydantic import BaseModel, Field
from typing import Optional

class Client(BaseModel):
    _id: Optional[str]
    id: Optional[str]
    name: str
    phone: str
    description: str
    email: str
    address: str
    named_as: str
    company_id: str    

