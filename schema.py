from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: str

class ProductResponse(ProductBase):
    id: int 

    class Config:
        from_attributes: bool = True

    