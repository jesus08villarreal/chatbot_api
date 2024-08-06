from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    named_has: str
    foreing_id: int

    class Config:
        from_attributes = True
