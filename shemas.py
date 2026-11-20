from pydantic import BaseModel, ConfigDict, Field


class ServicioCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: int = Field(gt=0)
    description: str = Field(min_length=10, max_length=200)


class ServicioResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str

    model_config = ConfigDict(from_attributes=True)