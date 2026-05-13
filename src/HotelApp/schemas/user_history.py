"""
Schemas Pydantic para la entidad UserHistory.

Reglas de negocio validadas aqui:
- action debe describir que hizo el usuario en el hotel (ej. Reserva, Check-in).
"""

from datetime import datetime

from pydantic import BaseModel, Field


class UserHistoryBase(BaseModel):
    """Campos comunes a todas las representaciones de UserHistory."""

    user_id: int = Field(
        ...,
        description="ID del usuario asociado a la accion.",
    )
    action: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Accion realizada por o para el cliente.",
        examples=["Check-in", "Cancelacion de reserva"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Detalles adicionales de la accion.",
    )


class UserHistoryCreate(UserHistoryBase):
    """Payload para registrar un evento en el historial (POST /user-history)."""


class UserHistoryResponse(UserHistoryBase):
    """Representacion de un registro de historial devuelto por la API."""

    id: int = Field(..., description="Identificador del registro.")
    timestamp: datetime = Field(..., description="Fecha y hora del registro.")

    model_config = {"from_attributes": True}