"""
Schemas Pydantic para la entidad Room.

Reglas de negocio validadas aqui:
- number_id: Identificador de la habitacion (ej. 101, 204A).
- price_per_night: Debe ser mayor que 0.
- status: Debe ser 'Disponible', 'Ocupada' o 'Mantenimiento'.
"""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class RoomBase(BaseModel):
    """Campos comunes a todas las representaciones de Room."""

    number_id: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Numero o identificador fisico de la habitacion.",
        examples=["101", "Suite A"],
    )
    room_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Tipo de habitacion.",
        examples=["Sencilla", "Doble", "Suite"],
    )
    price_per_night: Decimal = Field(
        ...,
        decimal_places=2,
        description="Precio por noche. Debe ser mayor que 0.",
        examples=[150000.00],
    )
    status: Literal["Disponible", "Ocupada", "Mantenimiento"] = Field(
        default="Disponible",
        description="Estado actual de la habitacion.",
    )

    @field_validator("price_per_night")
    @classmethod
    def price_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El precio por noche debe ser mayor que 0.")
        return v


class RoomCreate(RoomBase):
    """Payload para crear una nueva habitacion (POST /rooms)."""


class RoomUpdate(BaseModel):
    """Payload para actualizar una habitacion (PATCH o PUT /rooms/{id})."""

    number_id: str | None = Field(default=None, min_length=1, max_length=10)
    room_type: str | None = Field(default=None, min_length=2, max_length=50)
    price_per_night: Decimal | None = Field(default=None, decimal_places=2)
    status: Literal["Disponible", "Ocupada", "Mantenimiento"] | None = Field(default=None)

    @field_validator("price_per_night")
    @classmethod
    def price_must_be_positive(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v <= 0:
            raise ValueError("El precio por noche debe ser mayor que 0.")
        return v

    @model_validator(mode="after")
    def at_least_one_field(self) -> "RoomUpdate":
        if not any([self.number_id, self.room_type, self.price_per_night, self.status]):
            raise ValueError("Se debe enviar al menos un campo para actualizar.")
        return self


class RoomResponse(RoomBase):
    """Representacion de una habitacion devuelta por la API."""

    id: int = Field(..., description="Identificador unico de la habitacion en BD.")

    model_config = {"from_attributes": True}