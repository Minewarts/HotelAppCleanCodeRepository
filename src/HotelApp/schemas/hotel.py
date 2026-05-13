"""
Schemas Pydantic para la entidad Hotel.

Reglas de negocio validadas aqui:
- Dado que el sistema (HOT TEL) administra un unico hotel, no se requiere POST.
- Solo se define la actualizacion y lectura de su configuracion general.
"""

from pydantic import BaseModel, Field, model_validator


class HotelBase(BaseModel):
    """Campos comunes de la configuracion del unico hotel."""

    name: str = Field(
        default="HOT TEL",
        min_length=2,
        max_length=150,
        description="Nombre comercial del hotel.",
    )
    address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Direccion fisica de las instalaciones.",
    )
    phone: str = Field(
        ...,
        min_length=7,
        max_length=20,
        description="Telefono principal de contacto.",
    )


class HotelUpdate(BaseModel):
    """Payload para actualizar la informacion del hotel (PUT /hotel)."""

    name: str | None = Field(default=None, min_length=2, max_length=150)
    address: str | None = Field(default=None, min_length=5, max_length=200)
    phone: str | None = Field(default=None, min_length=7, max_length=20)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "HotelUpdate":
        if self.name is None and self.address is None and self.phone is None:
            raise ValueError(
                "Se debe enviar al menos un campo para actualizar la informacion del hotel."
            )
        return self


class HotelResponse(HotelBase):
    """Representacion de la configuracion del hotel devuelta por la API."""

    id: int = Field(..., description="Identificador del hotel (usualmente 1).")

    model_config = {"from_attributes": True}